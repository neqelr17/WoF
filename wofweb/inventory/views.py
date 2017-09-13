from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView


from . import models


# decorators = [login_required]
decorators = []

@method_decorator(decorators, name='dispatch')
class Index(View):
    initial = {'title': 'WoF'}
    template_name = 'inventory/index.html'

    def get(self, request):
        ctx = {'title': 'WoF Inventory'}
        return render(request, self.template_name, ctx)


class Items(ListView):
    model = models.Item
