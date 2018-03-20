from django.contrib import admin

# Register your models here.
from apps.facturas.models import Factura, Proveedor


@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['tipo_doc', 'nro_doc', 'nombre', 'habilitado']
    list_per_page = 15


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ['establecimiento', 'punto_expedicion', 'numero', 'fecha', 'tipo', 'timbrado', 'moneda']
    list_per_page = 15
