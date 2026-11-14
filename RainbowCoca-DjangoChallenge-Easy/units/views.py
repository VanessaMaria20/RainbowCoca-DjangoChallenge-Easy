from django.shortcuts import render, redirect
from .forms import UnitForm

def unit_create(request):
    if request.method == "POST":
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("unit_create")
    else:
        form = UnitForm(initial={"health": 100})
    return render(request, "units/unit_form.html", {"form": form})
# Create your views here.
