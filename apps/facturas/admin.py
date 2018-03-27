from django.contrib import admin

# Register your models here.
from apps.facturas.models import Proveedor, FacturaProveedor, FacturaProveedorDetalle


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['tipo_doc', 'nro_doc', 'nombre', 'habilitado']
    exclude = ['transaccion']
    list_per_page = 15


class FacturaDetalleInline(admin.StackedInline):
    """
    Clase StackedInline para hacer que en el admin de Factura aparezcan dos modelos: Factura y FacturaDetalle
    """
    model = FacturaProveedorDetalle


@admin.register(FacturaProveedor)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ['establecimiento', 'punto_expedicion', 'numero', 'fecha', 'tipo', 'timbrado', 'moneda']
    list_select_related = True
    list_per_page = 15
    exclude = ['transaccion']
    inlines = [FacturaDetalleInline]
