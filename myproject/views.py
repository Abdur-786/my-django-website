from django.shortcuts import render


def homepage(request):
    return render(request, 'home.html')


def animals(request):
    return render(request, 'animals.html')
