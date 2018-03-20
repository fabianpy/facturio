from django.db import models

# Create your models here.


class Tipo(models.Model):
    codigo = models.CharField(max_length=3)
    nombre = models.CharField(max_length=100)

    class Meta:
        abstract = True


class Moneda(Tipo):
    # hereda atributos 'codigo' y 'nombre' de la clase abstracta 'Tipo'
    decimales = models.IntegerField()  # TODO: usar validators de max y min value
    abreviatura = models.CharField(max_length=10)
    simbolo = models.CharField(max_length=10)
    habilitado = models.BooleanField(default=True)


class IVA(models.Model):
    porcentaje = models.DecimalField(max_digits=5, decimal_places=2)
    habilitado = models.BooleanField(default=True)
