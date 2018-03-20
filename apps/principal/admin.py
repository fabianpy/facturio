from django.contrib import admin

# Register your models here.
from apps.principal.models import Moneda


@admin.register(Moneda)
class MonedaAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'decimales', 'abreviatura', 'simbolo', 'habilitado']
    list_per_page = 15
