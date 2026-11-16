from django.contrib import admin

from .models import EnergyGoal, EnergySource, EnergyUsage

admin.site.register(EnergySource)
admin.site.register(EnergyUsage)
admin.site.register(EnergyGoal)
