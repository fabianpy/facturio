from django.db import models

# Create your models here.
from apps.principal.models import IVA, Moneda
from utils.choices import TIPO_DOC_CHOICES, TIPO_FACTURA_CHOICES


class Proveedor(models.Model):
    tipo_doc = models.CharField(max_length=3, choices=TIPO_DOC_CHOICES)
    nro_doc = models.CharField(max_length=30, choices=TIPO_DOC_CHOICES)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=30)
    email = models.EmailField()


class Factura(models.Model):
    establecimiento = models.IntegerField()
    punto_expedicion = models.IntegerField()
    numero = models.IntegerField()
    fecha = models.DateField(auto_now=False)
    tipo = models.CharField(max_length=2, choices=TIPO_FACTURA_CHOICES)
    timbrado = models.CharField(max_length=8)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE)


class FacturaDetalle(models.Model):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=21, decimal_places=3)
    monto_eq = models.DecimalField(max_digits=21, decimal_places=3)
    monto_iva = models.DecimalField(max_digits=21, decimal_places=3)
    monto_iva_eq = models.DecimalField(max_digits=21, decimal_places=3)
    iva = models.ForeignKey(IVA, on_delete=models.CASCADE)
