from django.core import serializers
from django.http.response import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls.base import reverse
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from apps.facturas.forms import ProveedorForm, FacturaProveedorForm
from apps.facturas.models import FacturaProveedor, Proveedor, FacturaProveedorDetalle, TimbradoProveedor
from apps.principal.models import IVA


def prueba(request):
    return render(request, 'facturas/ingresoFactura/list.html')


class ProveedorList(ListView):
    template_name = 'facturas/proveedores/list.html'
    model = Proveedor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Proveedores"
        return context


class ProveedorCreate(CreateView):
    template_name = 'facturas/proveedores/form.html'
    model = Proveedor
    form_class = ProveedorForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Nuevo proveedor"
        return context

    def get_success_url(self):
        return reverse('facturas:proveedores-editar', args=[self.object.id])


class ProveedorUpdate(UpdateView):
    template_name = 'facturas/proveedores/form.html'
    model = Proveedor
    form_class = ProveedorForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar proveedor"

        timbrados = TimbradoProveedor.objects.filter(proveedor=self.object.id).order_by('id')
        context['timbrados'] = timbrados
        return context

    def get_success_url(self):
        return reverse('facturas:proveedores-editar', args=[self.object.id])


class TimbradoProveedorView(View):

    def get(self, request, *args, **kwargs):
        timbrado = TimbradoProveedor.objects.get(pk=request.GET.get('id'))
        data = serializers.serialize('json', [timbrado])
        print("data ", data)
        return JsonResponse(data, safe=False)


class TimbradoProveedorCreate(View):

    def post(self, request, *args, **kwargs):
        print("llega al crear detalle", "es string?: ", isinstance(request.POST.get('proveedor'), str))
        proveedor = Proveedor.objects.get(pk=request.POST.get('proveedor'))
        print("id proveedor", proveedor.id, proveedor)
        timbrado_proveedor = TimbradoProveedor(proveedor=proveedor)
        timbrado_proveedor.timbrado = request.POST.get('timbrado')
        timbrado_proveedor.establecimiento = request.POST.get('establecimiento')
        timbrado_proveedor.punto_expedicion = request.POST.get('punto_expedicion')
        timbrado_proveedor.vigencia = request.POST.get('vigencia')
        timbrado_proveedor.vencimiento = request.POST.get('vencimiento')

        timbrado_proveedor.save()
        return JsonResponse({'success': True})


class TimbradoProveedorUpdate(View):

    def post(self, request):
        timbrado_proveedor = TimbradoProveedor.objects.get(pk=request.POST.get('id'))
        timbrado_proveedor.timbrado = request.POST.get('timbrado')
        timbrado_proveedor.establecimiento = request.POST.get('establecimiento')
        timbrado_proveedor.punto_expedicion = request.POST.get('punto_expedicion')
        timbrado_proveedor.vigencia = request.POST.get('vigencia')
        timbrado_proveedor.vencimiento = request.POST.get('vencimiento')

        timbrado_proveedor.save()
        return JsonResponse({'success': True})


class FacturaList(ListView):
    template_name = 'facturas/ingresoFactura/list.html'
    model = FacturaProveedor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Facturas de proveedores"
        return context


class FacturaProveedorCreate(CreateView):
    template_name = 'facturas/ingresoFactura/form.html'
    model = FacturaProveedor
    form_class = FacturaProveedorForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Nueva factura de proveedor"
        return context

    def get_success_url(self):
        return reverse('facturas:ingresoFactura-editar', args=[self.object.id])


class FacturaProveedorUpdate(UpdateView):
    template_name = 'facturas/ingresoFactura/form.html'
    model = FacturaProveedor
    form_class = FacturaProveedorForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar factura de proveedor"

        detalles = FacturaProveedorDetalle.objects.filter(factura=self.object.id)
        context['detalles_factura'] = detalles
        return context


class FacturaProveedorDetalleCreate(View):

    def post(self, request, *args, **kwargs):
        print("llega al crear detalle", "es string?: ", isinstance(request.POST.get('factura'), str))
        factura = FacturaProveedor.objects.get(pk=request.POST.get('factura'))
        print("id factura", factura.id, factura)
        factura_detalle = FacturaProveedorDetalle(factura=factura)
        factura_detalle.cantidad = request.POST.get('cantidad')
        factura_detalle.monto = request.POST.get('monto')
        factura_detalle.monto_eq = request.POST.get('monto')
        factura_detalle.iva = IVA.objects.get(pk=request.POST.get('iva'))
        factura_detalle.monto_iva = request.POST.get('monto_iva')
        factura_detalle.monto_iva_eq = request.POST.get('monto_iva')
        factura_detalle.descripcion = request.POST.get('descripcion')

        factura_detalle.save()
        return JsonResponse({'success': True})


class FacturaProveedorDetalleUpdate(View):

    def post(self, request, *args, **kwargs):
        factura_detalle = FacturaProveedorDetalle.objects.get(pk=request.POST.get('id'))
        factura_detalle.cantidad = request.POST.get('cantidad')
        factura_detalle.monto = request.POST.get('monto')
        factura_detalle.monto_eq = request.POST.get('monto')
        factura_detalle.iva = IVA.objects.get(pk=request.POST.get('iva'))
        factura_detalle.monto_iva = request.POST.get('monto_iva')
        factura_detalle.monto_iva_eq = request.POST.get('monto_iva')
        factura_detalle.descripcion = request.POST.get('descripcion')

        factura_detalle.save()
        return JsonResponse({'success': True})


class FacturaProveedorDetalleView(View):

    def get(self, request, *args, **kwargs):
        id_detalle = request.GET.get('id')
        factura_detalle = FacturaProveedorDetalle.objects.get(pk=id_detalle)
        data = serializers.serialize('json', [factura_detalle])
        return JsonResponse(data, safe=False)
