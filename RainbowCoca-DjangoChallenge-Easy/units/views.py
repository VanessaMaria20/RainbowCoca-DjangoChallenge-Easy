from django.shortcuts import render, redirect, get_object_or_404
from .forms import UnitForm
from .models import Unit


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
    return render(request, "units/unit_list.html", {"units": units})


def unit_detail(request, unit_id):
    unit = get_object_or_404(Unit, pk=unit_id)
    return render(request, "units/unit_detail.html", {"unit": unit})


def unit_heal(request, unit_id):
    if request.method == "POST":
        unit = get_object_or_404(Unit, pk=unit_id)
        unit.health = 100
        unit.save()
    return redirect("unit_list")