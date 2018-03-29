from django.urls.conf import path

from apps.facturas import views

urlpatterns = [
    path('ingresoFactura/', views.FacturaTemplate.as_view(), name="ingresoFactura"),
    # path('ingresoFactura/', views.prueba, name='prueba')
    path('proveedores/', views.ProveedorTemplate.as_view(), name="proveedores"),

]
