from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils.timezone import now

from facturio.middleware import get_current_user


class TipoBase(models.Model):
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
    CREACION_GRUPO_PROVEEDOR = 'CrGP'
    CONFIGURACION_INICIAL = 'ConI'
    TIPO_TRANSACCION_CHOICES = (
        (CONFIGURACION_INICIAL, 'Configuración Inicial'),
        (CREACION_PROVEEDOR, 'Creación de Proveedor'),
        (CREACION_FACTURA_PROVEEDOR, 'Creación de Factura de Proveedor'),
        (CREACION_GRUPO_PROVEEDOR, 'Creación de Grupo de Proveedor'),
    )

    tipo = models.CharField(max_length=4, choices=TIPO_TRANSACCION_CHOICES, null=False)
    estado = models.CharField(max_length=2, choices=ESTADO_TRANSACCION_CHOICES, null=False, default=ESTADO_VIGENTE)
    fecha = models.DateTimeField(default=now)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Transacción'
        verbose_name_plural = 'Transacciones'

    @classmethod
    def crear_transaccion(cls, tipo):
        transaccion = cls(tipo=tipo, usuario=get_current_user())
        transaccion.save()
        return transaccion


class EntidadBaseManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(transaccion__usuario=get_current_user())


class EntidadBase(models.Model):
    habilitado = models.BooleanField(default=True)
    transaccion = models.ForeignKey(Transaccion, on_delete=models.DO_NOTHING, null=False)
    objects = models.Manager()
    user_objects = EntidadBaseManager()

    class Meta:
        abstract = True
