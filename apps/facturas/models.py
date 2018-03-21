from django.db import models

# Create your models here.
from apps.principal.models import IVA, Moneda, BaseEntidad
from utils.choices import TIPO_DOC_CHOICES, TIPO_FACTURA_CHOICES


"""
IMPORTANTE:

Hacer que todos los modelos que representen la cabecera de una entidad hereden de la clase BaseEntidad
"""


class Proveedor(BaseEntidad):
    tipo_doc = models.CharField(max_length=3, choices=TIPO_DOC_CHOICES, default="RUC")
    nro_doc = models.CharField(max_length=30, null=False)
    nombre = models.CharField(max_length=100, null=False)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=30)
    email = models.EmailField()


class Factura(BaseEntidad):
    establecimiento = models.IntegerField(null=False)
    punto_expedicion = models.IntegerField(null=False)
    numero = models.IntegerField(null=False)
    fecha = models.DateField(auto_now=False, null=False)
    tipo = models.CharField(max_length=2, choices=TIPO_FACTURA_CHOICES, default="CON")
    timbrado = models.CharField(max_length=8, null=False)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE, null=False)


class FacturaDetalle(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=21, decimal_places=3, null=False)
    monto_eq = models.DecimalField(max_digits=21, decimal_places=3, null=False)
    monto_iva = models.DecimalField(max_digits=21, decimal_places=3, null=False)
    monto_iva_eq = models.DecimalField(max_digits=21, decimal_places=3, null=False)
    iva = models.ForeignKey(IVA, on_delete=models.CASCADE, null=False)
