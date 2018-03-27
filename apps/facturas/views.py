from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView

from apps.facturas.models import FacturaProveedor


def prueba(request):
    return render(request, 'facturas/ingresoFactura/main.html')


class FacturaTemplate(TemplateView):
    template_name = 'facturas/ingresoFactura/main.html'  # TODO: crear el html


class FacturaCreate(CreateView):
    model = FacturaProveedor
    template_name = 'facturas/ingresoFactura/form.html'  # TODO: crear el html