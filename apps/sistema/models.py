from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils.timezone import now


class BaseTipo(models.Model):
    codigo = models.CharField(max_length=3)
    nombre = models.CharField(max_length=100)

    class Meta:
        abstract = True


class TipoTransaccion(BaseTipo):
    pass


class Transaccion(models.Model):
    tipo = models.ForeignKey(TipoTransaccion, on_delete=models.CASCADE)
    fecha = models.DateField(default=now)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)


class BaseEntidad(models.Model):
    habilitado = models.BooleanField(default=True)
    transaccion = models.ForeignKey(Transaccion, on_delete=models.DO_NOTHING, null=True)  # TODO: Set not null when admin tests ends

    class Meta:
        abstract = True
