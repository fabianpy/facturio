from django.db import models

# Create your models here.
from apps.sistema.models import BaseTipo, BaseEntidad


class Moneda(BaseTipo, BaseEntidad):
    # hereda atributos 'codigo' y 'nombre' de la clase abstracta 'BaseTipo'
    decimales = models.IntegerField()  # TODO: usar validators de max y min value
    abreviatura = models.CharField(max_length=10)
    simbolo = models.CharField(max_length=10)


class IVA(BaseEntidad):
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
