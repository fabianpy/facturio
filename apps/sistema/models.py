from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils.timezone import now

from facturio.middleware import get_current_user


class BaseTipo(models.Model):
    codigo = models.CharField(max_length=3)
    nombre = models.CharField(max_length=100)

    class Meta:
        abstract = True


class Transaccion(models.Model):
    ESTADO_VIGENTE = 'VI'
    ESTADO_ANULADA = 'AN'
    ESTADO_TRANSACCION_CHOICES = (
        (ESTADO_VIGENTE, 'VIGENTE'),
        (ESTADO_ANULADA, 'ANULADA')
    )

    CREACION_PROVEEDOR = 'CrPr'
    CREACION_FACTURA_PROVEEDOR = 'CrFP'
    TIPO_TRANSACCION_CHOICES = (
        (CREACION_PROVEEDOR, 'Creación de Proveedor'),
        (CREACION_FACTURA_PROVEEDOR, 'Creación de Factura de Proveedor'),
    )

    tipo = models.CharField(max_length=4, choices=TIPO_TRANSACCION_CHOICES, null=False)
    estado = models.CharField(max_length=2, choices=ESTADO_TRANSACCION_CHOICES, null=False, default=ESTADO_VIGENTE)
    fecha = models.DateTimeField(default=now)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Transacción'
        verbose_name_plural = 'Transacciones'

    @classmethod
    def crear_transaccion(cls, tipo, usuario):
        transaccion = cls(tipo=tipo, usuario=usuario)
        transaccion.save()
        return transaccion


class BaseEntidadManager(models.Manager):

    def get_queryset(self):
        print("current user", get_current_user())
        return super().get_queryset().filter(transaccion__usuario=get_current_user())


class BaseEntidad(models.Model):
    habilitado = models.BooleanField(default=True)
    transaccion = models.ForeignKey(Transaccion, on_delete=models.DO_NOTHING, null=True)  # TODO: Set not null when admin tests ends
    user_objects = BaseEntidadManager()

    class Meta:
        abstract = True

