from django.shortcuts import render


def index(request):
    ctx = {}
    ctx['title'] = 'WoF Inventory'
    return render(request, 'inventory/index.html', ctx)
