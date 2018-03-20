from django.contrib import admin

# Register your models here.
from apps.principal.models import Moneda, IVA


@admin.register(Moneda)
class MonedaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'decimales', 'abreviatura', 'simbolo', 'habilitado']
    list_per_page = 15


@admin.register(IVA)
class IVAAdmin(admin.ModelAdmin):
    list_display = ['porcentaje', 'habilitado']
    list_per_page = 15
