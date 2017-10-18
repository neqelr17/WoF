from django.shortcuts import render


# Create your views here.
def index(request):
    ctx = {'title': 'WoF'}
    return render(request, 'home/index.html', ctx)
