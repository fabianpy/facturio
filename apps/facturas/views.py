from django.shortcuts import render

# Create your views here.
from django.urls.base import reverse
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from apps.facturas.forms import ProveedorForm, FacturaProveedorForm
from apps.facturas.models import FacturaProveedor, Proveedor


def prueba(request):
    return render(request, 'facturas/ingresoFactura/list.html')


class ProveedorList(ListView):
    template_name = 'facturas/proveedores/list.html'
    model = Proveedor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['card_title'] = "Proveedores"
        return context


class ProveedorCreate(CreateView):
    template_name = 'facturas/proveedores/form.html'
    model = Proveedor
    form_class = ProveedorForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['card_title'] = "Nuevo proveedor"
        return context


class ProveedorUpdate(UpdateView):
    template_name = 'facturas/proveedores/form.html'
    model = Proveedor
    form_class = ProveedorForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['card_title'] = "Editar proveedor"
        return context


class FacturaList(ListView):
    template_name = 'facturas/ingresoFactura/list.html'
    model = FacturaProveedor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['card_title'] = "Facturas de proveedores"
        return context


class FacturaProveedorCreate(CreateView):
    template_name = 'facturas/ingresoFactura/form.html'
    model = FacturaProveedor
    form_class = FacturaProveedorForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['card_title'] = "Nueva factura de proveedor"
        return context

    def get_success_url(self):
        return reverse('facturas:ingresoFactura-editar', args=[self.object.id])


class FacturaUpdate(UpdateView):
    template_name = 'facturas/ingresoFactura/form.html'
    model = FacturaProveedor
    form_class = FacturaProveedorForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['card_title'] = "Editar factura de proveedor"
        return context