from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class EnergySource(models.Model):
    source_ID = models.AutoField(primary_key=True)
    sourceType = models.CharField(max_length=100)
    energyCost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.sourceType


class EnergyUsage(models.Model):
    usage_ID = models.AutoField(primary_key=True)
    user_ID = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='energy_usages',
    )
    source_ID = models.ForeignKey(
        EnergySource,
        on_delete=models.CASCADE,
        related_name='usage_sources',
    )
    date = models.DateField()
    energyConsumed = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    def __str__(self):
        return f'Usage on {self.date} - {self.energyConsumed} kWh'


class EnergyGoal(models.Model):
    goal_ID = models.AutoField(primary_key=True)
    user_ID = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='energy_goals',
    )
    targetDate = models.DateField()
    targetConsumption = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    def __str__(self):
        return f'Goal by {self.targetDate}: {self.targetConsumption} kWh'
