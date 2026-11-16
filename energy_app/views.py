from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum
from django.shortcuts import redirect, render

from .forms import EnergyUsageForm
from .models import EnergyUsage


@login_required
def energy_usage_tracking(request):
    usages = (
        EnergyUsage.objects
        .filter(user_ID=request.user)
        .select_related('source_ID')
        .order_by('-date', '-usage_ID')
    )
    aggregates = usages.aggregate(
        total_consumption=Sum('energyConsumed'),
        average_consumption=Avg('energyConsumed'),
    )

    return render(request, 'energy_app/energy_usage_tracking.html', {
        'usages': usages,
        'total_consumption': aggregates['total_consumption'] or 0,
        'average_consumption': aggregates['average_consumption'] or 0,
    })


@login_required
def add_energy_usage_view(request):
    form = EnergyUsageForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        usage = form.save(commit=False)
        usage.user_ID = request.user
        usage.save()
        messages.success(request, 'Energy usage added successfully.')
        return redirect('energy_app:energy_tracking')

    return render(request, 'energy_app/add_energy_usage.html', {'form': form})
