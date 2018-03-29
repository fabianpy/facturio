from django.shortcuts import render

# Create your views here.
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from apps.facturas.forms import ProveedorForm
from apps.facturas.models import FacturaProveedor, Proveedor


def prueba(request):
    return render(request, 'facturas/ingresoFactura/main.html')


# class ProveedorTemplate(TemplateView):
#     template_name = 'facturas/proveedores/main.html'

class ProveedorTemplate(ListView):
    template_name = 'facturas/proveedores/main.html'
    model = Proveedor


class FacturaTemplate(TemplateView):
    template_name = 'facturas/ingresoFactura/main.html'  # TODO: crear el html


class FacturaCreate(CreateView):
    model = FacturaProveedor
    template_name = 'facturas/ingresoFactura/form.html'  # TODO: crear el html
