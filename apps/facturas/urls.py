from django.urls.conf import path

from apps.facturas import views

app_name = 'facturas'
urlpatterns = [
    path('ingresoFactura/', views.FacturaList.as_view(), name="ingresoFactura"),
    path('ingresoFactura/crear', views.FacturaProveedorCreate.as_view(), name="ingresoFactura-crear"),
    path('ingresoFactura/<int:pk>/editar', views.FacturaProveedorUpdate.as_view(), name="ingresoFactura-editar"),
    path('ingresoFactura/detalle/<int:pk>', views.FacturaProveedorDetalleView.as_view(), name="ingresoFactura-detalle"),
    path('ingresoFactura/detalle/crear', views.FacturaProveedorDetalleCreate.as_view(),
         name="ingresoFactura-detalle-crear"),
    path('ingresoFactura/detalle/editar', views.FacturaProveedorDetalleUpdate.as_view(),
         name="ingresoFactura-detalle-editar"),
    path('ingresoFactura/timbradoProveedor', views.TimbradoProveedorView.as_view(),  # POST
         name="ingresoFactura-timbrado-proveedor"),


    path('proveedores/', views.ProveedorList.as_view(), name="proveedores"),
    path('proveedores/crear', views.ProveedorCreate.as_view(), name="proveedores-crear"),
    path('proveedores/<int:pk>/editar', views.ProveedorUpdate.as_view(), name="proveedores-editar"),
    path('proveedores/timbrado/<int:pk>', views.TimbradoProveedorView.as_view(), name="proveedores-timbrado"),  # GET
    path('proveedores/timbrado/crear', views.TimbradoProveedorCreate.as_view(), name="proveedores-timbrado-crear"),
    path('proveedores/timbrado/editar', views.TimbradoProveedorUpdate.as_view(), name="proveedores-timbrado-editar"),

]
