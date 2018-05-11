from django.urls.conf import path

from apps.facturas import views

app_name = 'facturas'
urlpatterns = [
    path('ingresoFactura/', views.FacturaList.as_view(), name="ingresoFactura"),
    path('ingresoFactura/crear', views.FacturaProveedorCreate.as_view(), name="ingresoFactura-crear"),
    path('ingresoFactura/<int:pk>/editar', views.FacturaUpdate.as_view(), name="ingresoFactura-editar"),
    path('proveedores/', views.ProveedorList.as_view(), name="proveedores"),
    path('proveedores/crear', views.ProveedorCreate.as_view(), name="proveedores-crear"),
    path('proveedores/<int:pk>/editar', views.ProveedorUpdate.as_view(), name="proveedores-editar"),

]
