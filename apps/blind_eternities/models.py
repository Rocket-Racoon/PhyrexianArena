import uuid
from django.db import models
from config.constants import *


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
    
    
class Set(models.Model):
    id = models.URLField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    object = models.CharField(max_length=25, default='set')
    # -- CODES --
    code = models.CharField(
        max_length=10, 
        unique=True,
        db_index=True,
        help_text="Set Code"
    )
    mtgo_code = models.CharField(max_length=10, null=True, blank=True)
    arena_code = models.CharField(max_length=10, null=True, blank=True)
    tcgplayer_id = models.PositiveIntegerField(null=True, blank=True)
    # -- METADATA --
    name = models.CharField(max_length=300)
    set_type = models.CharField(
        max_length=50, 
        db_index=True
    )
    released_at = models.DateField(null=True, blank=True, db_index=True)
    block = models.CharField(max_length=300, null=True, blank=True)
    block_code = models.CharField(
        max_length=10, 
        null=True, 
        blank=True,
        db_index=True,
        help_text="Block Code"
    )
    parent_set_code = models.CharField(
        max_length=6,
        null=True,
        blank=True,
        db_index=True,
        help_text="Parent set code"
    )
    card_count = models.PositiveIntegerField(default=0)
    printed_size = models.PositiveIntegerField(null=True, blank=True)
    # -- FLAGS --
    digital = models.BooleanField(default=False)
    nonfoil_only = models.BooleanField(default=False)
    foil_only = models.BooleanField(default=False)
    has_commanders = models.BooleanField(default=True)
    # -- URIS --
    uri = models.URLField(max_length=500, blank=True, null=True)
    scryfall_uri = models.URLField(max_length=500, blank=True, null=True)
    search_uri = models.URLField(max_length=500, blank=True, null=True)
    # -- IMGs --
    icon_svg_uri = models.URLField(max_length=500, blank=True, null=True)
    