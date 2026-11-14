from django.urls import path
from . import views

urlpatterns = [
    path("unit/", views.unit_create, name="unit_create"),
]