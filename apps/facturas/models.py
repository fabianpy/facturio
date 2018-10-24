from django.db import models

# Create your models here.
from django.db.models.aggregates import Sum
from django.db.models.expressions import Case, When
from django.db.models.query_utils import Q

from apps.personas.models import Persona
from apps.principal.models import IVA, Moneda, EntidadBase
from apps.sistema.models import EntidadBaseManager
from utils.choices import TIPO_DOC_CHOICES, TIPO_FACTURA_CHOICES
from utils.funciones import formatear_documento

"""
IMPORTANTE:

Hacer que todos los modelos que representen la cabecera de una entidad hereden de la clase EntidadBase
"""


class FacturaBaseManager(EntidadBaseManager):

    def get_queryset(self):
        return super().get_queryset().annotate(
            monto_10=Sum(Case(
                When(Q(facturaproveedordetalle__iva=1), then='facturaproveedordetalle__monto'),  # 10
                default=0
            )),
            monto_5=Sum(Case(
                When(Q(facturaproveedordetalle__iva=2), then='facturaproveedordetalle__monto'),  # 5
                default=0
            )),
            iva_10=Sum(Case(
                When(Q(facturaproveedordetalle__iva=1), then='facturaproveedordetalle__monto_iva'),  # 10
                default=0
            )),
            iva_5=Sum(Case(
                When(Q(facturaproveedordetalle__iva=2), then='facturaproveedordetalle__monto_iva'),  # 5
                default=0
            )),
            exenta=Sum(Case(
                When(Q(facturaproveedordetalle__iva=3), then='facturaproveedordetalle__monto'),  # Ex
                default=0
            )),
        )


class FacturaBase(EntidadBase):
    """
    Clase abstracta para facturas de compras y ventas
    """
    establecimiento = models.IntegerField(null=False)
    punto_expedicion = models.IntegerField(null=False)
    numero = models.IntegerField(null=False)
    fecha = models.DateField(auto_now=False, null=False)
    tipo = models.CharField(max_length=2, choices=TIPO_FACTURA_CHOICES, default="CON")
    timbrado = models.CharField(max_length=8, null=False)
    moneda = models.ForeignKey(Moneda, on_delete=models.CASCADE, null=False, default=1)
    factura_objects = FacturaBaseManager()

    class Meta:
        abstract = True
        unique_together = ('timbrado', 'establecimiento', 'punto_expedicion', 'numero')

    def numero_formateado(self):
        return '{}-{}-{}'.format(self.establecimiento.__str__().zfill(3), self.punto_expedicion.__str__().zfill(3),
                                 self.numero.__str__().zfill(8))


class FacturaDetalleBase(models.Model):
    """
    Clase abstracta para detalles de facturas de compras y de ventas
    """
    cantidad = models.IntegerField(default=1, null=False)
    monto = models.DecimalField(max_digits=15, decimal_places=3, null=False)
    monto_eq = models.DecimalField(max_digits=15, decimal_places=3, null=False, verbose_name="Monto equivalente")
    iva = models.ForeignKey(IVA, on_delete=models.CASCADE, null=False)
    monto_iva = models.DecimalField(max_digits=15, decimal_places=3, null=False)
    monto_iva_eq = models.DecimalField(max_digits=15, decimal_places=3, null=False,
                                       verbose_name="Monto IVA equivalente")
    descripcion = models.CharField(max_length=512, blank=True, null=True, verbose_name="Descripción")

    class Meta:
        abstract = True


class ParametroFacturaBase(models.Model):
    timbrado = models.CharField(max_length=8, null=False)
    establecimiento = models.IntegerField(null=False)
    punto_expedicion = models.IntegerField(null=False)
    vigencia = models.DateField(auto_now=False, null=False)
    vencimiento = models.DateField(auto_now=False, null=False)
    vigente = models.BooleanField(default=True)

    class Meta:
        abstract = True


class ParametroFactura(ParametroFacturaBase):
    numero_inicial = models.IntegerField(null=False)
    numero_actual = models.IntegerField(null=True)  # último número generado
    cantidad = models.IntegerField(null=False)  # cantidad de facturas del talonario

    def __str__(self):
        return '{}-{}'.format(self.establecimiento.__str__().zfill(3), self.punto_expedicion.__str__().zfill(3))


class Factura(FacturaBase):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    parametro_factura = models.ForeignKey(ParametroFactura, on_delete=models.CASCADE)

    class Meta:
        ordering = ['fecha']

    def __str__(self):
        return self.numero_formateado()


class FacturaDetalle(FacturaDetalleBase):
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE, null=False)


class GrupoProveedor(EntidadBase):
    nombre = models.CharField(max_length=100, null=False)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Proveedor(EntidadBase):
    tipo_doc = models.CharField(max_length=3, choices=TIPO_DOC_CHOICES, null=False, default="RUC")
    nro_doc = models.CharField(max_length=30, null=False)
    nombre = models.CharField(max_length=100, null=False)
    direccion = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    grupo = models.ForeignKey(GrupoProveedor, on_delete=models.CASCADE)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return '({} - {}) {}'.format(self.tipo_doc, self.nro_doc, self.nombre)

    def documento_formateado(self):
        return formatear_documento(self.tipo_doc, self.nro_doc)


class TimbradoProveedor(ParametroFacturaBase):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)


class FacturaProveedor(FacturaBase):
    """
    Facturas de compras
    """
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __str__(self):
        return self.numero_formateado()


class FacturaProveedorDetalle(FacturaDetalleBase):
    factura = models.ForeignKey(FacturaProveedor, on_delete=models.CASCADE, null=False)
