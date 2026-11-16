from django import forms

from .models import EnergyUsage


class EnergyUsageForm(forms.ModelForm):
    class Meta:
        model = EnergyUsage
        fields = ['date', 'source_ID', 'energyConsumed']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'energyConsumed': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
        }
