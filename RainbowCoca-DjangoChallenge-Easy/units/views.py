import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UnitForm
from .models import Unit, Fight, FightStep
from django.db.models import Q, Sum

def unit_create(request):
    if request.method == "POST":
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("unit_create")
    else:
        form = UnitForm(initial={"health": 100})
    return render(request, "units/unit_form.html", {"form": form})


def unit_list(request):
    units = Unit.objects.all()
    stats = []
    for team, _ in Unit.Team.choices:
        stats.append({
            "team": team,
            "fights": Fight.objects.filter(Q(unit1__team=team) | Q(unit2__team=team)).count(),
            "damage_caused": FightStep.objects.filter(attacker__team=team).aggregate(s=Sum("damage"))["s"] or 0,
            "damage_taken": FightStep.objects.filter(defender__team=team).aggregate(s=Sum("damage"))["s"] or 0,
        })
    return render(request, "units/unit_list.html", {"units": units, "stats": stats})


def unit_detail(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    fights = (
        Fight.objects.filter(Q(unit1=unit) | Q(unit2=unit))
        .select_related("unit1", "unit2", "winner")
        .prefetch_related("steps__attacker", "steps__defender")
        .order_by("-created_at")
    )
    return render(request, "units/unit_detail.html", {"unit": unit, "fights": fights})

def unit_heal(request, unit_id):
    if request.method == "POST":
        unit = get_object_or_404(Unit, pk=unit_id)
        unit.health = 100
        unit.save()
    return redirect("unit_list")
def simulate_fight(request):
    if request.method != "POST":
        return redirect("unit_list")

    units = list(Unit.objects.filter(pk__in=request.POST.getlist("units")))
    if len(units) != 2:
        messages.error(request, "Select exactly 2 units.")
        return redirect("unit_list")

    u1, u2 = units
    if u1.team == u2.team:
        messages.error(request, "The units must be from different teams.")
        return redirect("unit_list")
    if u1.health == 0 or u2.health == 0:
        messages.error(request, "A unit with 0 health cannot fight. Heal it first.")
        return redirect("unit_list")
    if u1.attack_points == 0 and u2.attack_points == 0:
        messages.error(request, "Both units have 0 attack points, the fight would never end.")
        return redirect("unit_list")

    fight = Fight.objects.create(unit1=u1, unit2=u2)
    attacker, defender = u1, u2
    order = 1
    while u1.health > 0 and u2.health > 0:
        damage = random.randint(0, attacker.attack_points)
        defender.health = max(0, defender.health - damage)
        FightStep.objects.create(
            fight=fight,
            order=order,
            attacker=attacker,
            defender=defender,
            damage=damage,
            attacker_health=attacker.health,
            defender_health=defender.health,
        )
        order += 1
        attacker, defender = defender, attacker

    u1.save()
    u2.save()
    fight.winner = u1 if u1.health > 0 else u2
    fight.save()

    messages.success(request, f"{fight.winner.name} won after {order - 1} attacks.")
    return redirect("unit_list")