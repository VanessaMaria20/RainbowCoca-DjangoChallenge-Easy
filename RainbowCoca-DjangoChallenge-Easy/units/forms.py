from django import forms
from .models import Unit

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ["name", "type", "team", "health", "attack_points", "profile_image_link"]