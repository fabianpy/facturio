from django.contrib import admin

# Register your models here.
from apps.principal.models import Moneda, IVA


@admin.register(Moneda)
class MonedaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'decimales', 'abreviatura', 'simbolo', 'habilitado']
    exclude = ['transaccion']
    list_per_page = 15


@admin.register(IVA)
class IVAAdmin(admin.ModelAdmin):
    list_display = ['porcentaje', 'habilitado']
    exclude = ['transaccion']
    list_per_page = 15
