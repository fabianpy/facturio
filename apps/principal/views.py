from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView


class MainView(LoginRequiredMixin, TemplateView):
    template_name = 'apps/principal/index.html'
