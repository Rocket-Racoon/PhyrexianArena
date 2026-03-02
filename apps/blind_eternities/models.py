from django.db import models
from config.constants import *

# Create your models here.
class CreatureType(models.Model):
    """
    Catálogo dinámico de tipos de criatura.
    Se actualiza vía API para evitar mantenimiento manual.
    """
    name = models.CharField(max_length=100, unique=True, db_index=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Creature Type"

    def __str__(self):
        return self.name