from django.db import models

# Create your models here.
from apps.sistema.models import BaseEntidad
from utils.choices import TIPO_DOC_CHOICES


class Persona(BaseEntidad):
    FISICA = 'F'
    JURIDICA = 'J'
    TIPO_PERSONA_CHOICES = (
        (FISICA, 'Física'),
        (JURIDICA, 'Jurídica'),
    )
    nombres = models.CharField(max_length=255, null=False, blank=True)
    apellidos = models.CharField(max_length=255, null=True, blank=True)
    tipo_doc = models.CharField(max_length=3, choices=TIPO_DOC_CHOICES, null=False, default='RUC')
    nro_doc = models.CharField(max_length=30, null=False, blank=False)
    tipo_persona = models.CharField(max_length=1, choices=TIPO_PERSONA_CHOICES, default=JURIDICA)

    class Meta:
        ordering = ['apellidos', 'nombres', 'id']
