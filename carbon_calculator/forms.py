from django import forms


class CarbonCalculatorForm(forms.Form):
    DIET_CHOICES = [
        ('omnivore', 'Omnivore'),
        ('vegetarian/vegan', 'Vegetarian/Vegan'),
    ]
    TRANSPORT_CHOICES = [
        ('car', 'Car'),
        ('public transport', 'Public Transport'),
        ('bike or walking', 'Bike or Walking'),
    ]

    diet = forms.ChoiceField(choices=DIET_CHOICES, widget=forms.RadioSelect)
    transport = forms.ChoiceField(choices=TRANSPORT_CHOICES, widget=forms.RadioSelect)
    people = forms.IntegerField(min_value=1, max_value=10, initial=1)
