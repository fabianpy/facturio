from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls.base import reverse
from django.views.generic.base import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from apps.facturas.forms import ProveedorForm, FacturaProveedorForm, GrupoProveedorForm
from apps.facturas.models import FacturaProveedor, Proveedor, FacturaProveedorDetalle, TimbradoProveedor, GrupoProveedor
from apps.principal.models import IVA
from apps.sistema.models import Transaccion
from facturio.middleware import get_current_user


def prueba(request):
    return render(request, 'apps/facturas/ingresoFactura/list.html')


class GrupoProveedorList(LoginRequiredMixin, ListView):
    template_name = 'apps/facturas/grupoProveedor/list.html'
    model = GrupoProveedor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Grupos de Proveedores"
        return context

    def get_queryset(self):
        qs = GrupoProveedor.user_objects.all()
        return qs


class GrupoProveedorCreate(LoginRequiredMixin, CreateView):
    template_name = 'apps/facturas/grupoProveedor/form.html'
    model = GrupoProveedor
    form_class = GrupoProveedorForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Nuevo grupo de proveedor"
        return context

    def get_success_url(self):
        return reverse('facturas:grupo-proveedor-editar', args=[self.object.id])

    def form_valid(self, form):
        form.instance.transaccion = Transaccion.crear_transaccion(Transaccion.CREACION_PROVEEDOR)
        return super().form_valid(form)


class GrupoProveedorUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'apps/facturas/grupoProveedor/form.html'
    model = GrupoProveedor
    form_class = GrupoProveedorForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar grupo de proveedor"
        return context

    def get_success_url(self):
        return reverse('facturas:grupo-proveedor-editar', args=[self.object.id])


class ProveedorList(LoginRequiredMixin, ListView):
    template_name = 'apps/facturas/proveedores/list.html'
    model = Proveedor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Proveedores"
        return context

    def get_queryset(self):
        qs = Proveedor.user_objects.all()
        return qs


class ProveedorCreate(LoginRequiredMixin, CreateView):
    template_name = 'apps/facturas/proveedores/form.html'
    model = Proveedor
    form_class = ProveedorForm

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs.update({
    #         'user': self.request.user
    #     })
    #     return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Nuevo proveedor"
        return context

    def get_success_url(self):
        return reverse('facturas:proveedores-editar', args=[self.object.id])

    def form_valid(self, form):
        form.instance.transaccion = Transaccion.crear_transaccion(Transaccion.CREACION_PROVEEDOR)
        return super().form_valid(form)


class ProveedorUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'apps/facturas/proveedores/form.html'
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
        """
        Método usado en CRUD de proveedores, para obtener los datos del timbrado seleccionado para su edición.
        """
        timbrado = TimbradoProveedor.objects.get(pk=request.GET.get('id'))
        data = serializers.serialize('json', [timbrado])
        return JsonResponse(data, safe=False)

    def post(self, request):
        """
        Método usado en ingreso de facturas de proveedores para retornar los datos del proveedor a través del timbrado,
        de manera a autocompletar los campos del formulario.
        """
        timbrado = request.POST.get('timbrado')
        try:
            timbrado_proveedor = TimbradoProveedor.objects.get(timbrado=timbrado, proveedor__transaccion__usuario=get_current_user())
            data = serializers.serialize('json', [timbrado_proveedor])
            return JsonResponse(data, safe=False)
        except ObjectDoesNotExist:
            timbrado_proveedor = TimbradoProveedor()
            data = serializers.serialize('json', [timbrado_proveedor])
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


class FacturaProveedorList(LoginRequiredMixin, ListView):
    template_name = 'apps/facturas/ingresoFactura/list.html'
    model = FacturaProveedor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Facturas de proveedores"
        return context

    def get_queryset(self):
        qs = FacturaProveedor.user_objects.all()
        return qs


class FacturaProveedorCreate(LoginRequiredMixin, CreateView):
    template_name = 'apps/facturas/ingresoFactura/form.html'
    model = FacturaProveedor
    form_class = FacturaProveedorForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Nueva factura de proveedor"
        return context

    def get_success_url(self):
        return reverse('facturas:ingresoFactura-editar', args=[self.object.id])

    def form_valid(self, form):
        print("form is valid")
        form.instance.transaccion = Transaccion.crear_transaccion(Transaccion.CREACION_FACTURA_PROVEEDOR)
        return super().form_valid(form)

    def form_invalid(self, form):
        print("form is INvalid", form.errors)
        return super().form_invalid(form)


class FacturaProveedorCreateRapido(LoginRequiredMixin, CreateView):
    template_name = 'apps/facturas/ingresoFactura/form_rapido.html'
    model = FacturaProveedor
    form_class = FacturaProveedorForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Nueva factura de proveedor"
        return context

    def get_success_url(self):
        return reverse('facturas:ingresoFactura-editar', args=[self.object.id])

    def form_valid(self, form):
        print("form is valid")
        form.instance.transaccion = Transaccion.crear_transaccion(Transaccion.CREACION_FACTURA_PROVEEDOR)
        return super().form_valid(form)

    def form_invalid(self, form):
        print("form is INvalid", form.errors)
        return super().form_invalid(form)


class FacturaProveedorUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'apps/facturas/ingresoFactura/form.html'
    model = FacturaProveedor
    form_class = FacturaProveedorForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Editar factura de proveedor"

        detalles = FacturaProveedorDetalle.objects.filter(factura=self.object.id)
        context['detalles_factura'] = detalles
        return context

    def get_success_url(self):
        return reverse('facturas:ingresoFactura-editar', args=[self.object.id])


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
