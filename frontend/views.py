from django.shortcuts import render


def react_fronted(request, *args, **kwargs):
    return render(request, 'frontend/index.html')
