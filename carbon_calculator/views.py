from django.shortcuts import render

from .forms import CarbonCalculatorForm


def carbon_calculator(request):
    result = None
    form = CarbonCalculatorForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        diet_impact = {'omnivore': 3, 'vegetarian/vegan': 1}
        transport_impact = {'car': 5, 'public transport': 2, 'bike or walking': 0}

        diet = form.cleaned_data['diet']
        transport = form.cleaned_data['transport']
        people = form.cleaned_data['people']

        result = round((diet_impact[diet] + transport_impact[transport]) / people, 2)

    return render(request, 'carbon_calculator/carbon_calculator.html', {
        'form': form,
        'result': result,
    })
