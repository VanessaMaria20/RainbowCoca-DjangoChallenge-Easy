from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Unit(models.Model):
    class UnitType(models.TextChoices):
        INFANTRY = "Infantry"
        CANNON = "Cannon"
        CAVALRY = "Cavalry"
        KNIGHT = "Knight"

    class Team(models.TextChoices):
        BLUE = "Blue"
        RED = "Red"

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=UnitType.choices)
    team = models.CharField(max_length=10, choices=Team.choices)
    health = models.IntegerField(
        default=100,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    attack_points = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(50)],
    )
    profile_image_link = models.URLField()

    def __str__(self):
        return f"{self.name} ({self.team})"
# Create your models here.
