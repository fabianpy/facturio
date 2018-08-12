from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView


class MainView(TemplateView):
    template_name = 'apps/principal/index.html'
