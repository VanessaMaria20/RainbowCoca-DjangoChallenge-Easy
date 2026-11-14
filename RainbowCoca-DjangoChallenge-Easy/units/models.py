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
class Fight(models.Model):
    unit1 = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="fights_as_unit1")
    unit2 = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="fights_as_unit2")
    winner = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, related_name="fights_won")
    created_at = models.DateTimeField(auto_now_add=True)


class FightStep(models.Model):
    fight = models.ForeignKey(Fight, on_delete=models.CASCADE, related_name="steps")
    order = models.PositiveIntegerField()
    attacker = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="attacks")
    defender = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="defenses")
    damage = models.PositiveIntegerField()
    attacker_health = models.IntegerField()
    defender_health = models.IntegerField()

    class Meta:
        ordering = ["order"]
# Create your models here.
