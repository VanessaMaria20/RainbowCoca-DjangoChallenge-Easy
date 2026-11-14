from django.urls import path
from . import views

urlpatterns = [
    path("unit/", views.unit_create, name="unit_create"),
    path("unit/all/", views.unit_list, name="unit_list"),
    path("unit/<int:unit_id>/", views.unit_detail, name="unit_detail"),
    path("unit/<int:unit_id>/heal/", views.unit_heal, name="unit_heal"),
    path("unit/simulate/", views.simulate_fight, name="simulate_fight"),
]