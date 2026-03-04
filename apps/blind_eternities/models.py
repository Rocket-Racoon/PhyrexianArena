import uuid
from django.db import models
from config.constants import *


# -- TYPES
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


# -- SETS --    
class Set(models.Model):
    id = models.URLField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    object = models.CharField(max_length=25, default='set')
    # -- CODES --
    code = models.CharField(
        max_length=10, 
        unique=False,
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


# -- CARDS --
class Card(models.Model):
    # --- CORE IDS ---
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    oracle_id = models.UUIDField(db_index=True, null=True, blank=True)
    arena_id = models.IntegerField(blank=True, null=True)
    mtgo_id = models.IntegerField(blank=True, null=True)
    mtgo_foil_id = models.IntegerField(blank=True, null=True)
    multiverse_ids = models.JSONField(default=list)
    resource_id = models.CharField(max_length=100, blank=True, null=True)
    tcgplayer_id = models.IntegerField(null=True, blank=True)
    tcgplayer_etched_id = models.IntegerField(null=True, blank=True)
    cardmarket_id = models.IntegerField(null=True, blank=True)
    
    # -- METADATA --
    object = models.CharField(max_length=50, default='card')
    lang = models.CharField(max_length=10, default='en')
    layout = models.CharField(max_length=50, null=True, blank=True)
    
    is_banned = models.BooleanField(default=False)
    is_restricted = models.BooleanField(default=False)
    is_token = models.BooleanField(default=False)
    is_emblem = models.BooleanField(default=False)
    can_be_commander = models.BooleanField(
        default=False, 
        db_index=True, 
        help_text="Whether this card is legal to be used as a commander"
    )
    can_have_multiple_copies = models.BooleanField(
        default=False,
        help_text="Whether this card can have multiple copies in a deck"
    )
    max_copies_in_deck = models.PositiveSmallIntegerField(
        default=1,
        help_text="Maximum number of copies allowed in a deck by card rules"
    )
    banned_as_companion = models.BooleanField(default=False)
    
    # -- DATA --
    name = models.CharField(max_length=255, null=True, blank=True)
    printed_name = models.CharField(max_length=255, blank=True, null=True)
    oracle_text = models.TextField(blank=True, null=True)
    printed_text = models.TextField(blank=True, null=True)
    type_line = models.CharField(max_length=255, blank=True, null=True)
    printed_type_line = models.CharField(max_length=255, blank=True, null=True)
    keywords = models.JSONField(default=list, blank=True, null=True)
    cmc = models.FloatField(default=0.0, blank=True, null=True)
    mana_cost = models.CharField(max_length=255, blank=True, null=True)
    power = models.CharField(max_length=10, null=True, blank=True)
    toughness = models.CharField(max_length=10, null=True, blank=True)
    loyalty = models.CharField(max_length=10, null=True, blank=True)
    defense = models.CharField(max_length=10, null=True, blank=True)
    attraction_lights = models.JSONField(default=list, null=True, blank=True)
    colors = models.JSONField(null=True, blank=True)
    color_identity = models.JSONField(default=list)
    color_indicator = models.JSONField(null=True, blank=True)
    produced_mana = models.JSONField(null=True, blank=True)
    reserved = models.BooleanField(default=False)
    game_changer = models.BooleanField(null=True, blank=True)
    flavor_name = models.CharField(max_length=255, null=True, blank=True)
    available_languages = models.JSONField(default=list, blank=True)
    
    # -- VANGUARD --
    hand_modifier = models.CharField(max_length=10, null=True, blank=True)
    life_modifier = models.CharField(max_length=10, null=True, blank=True)
    
    # -- RANK DATA --
    edhrec_rank = models.IntegerField(null=True, blank=True)
    penny_rank = models.IntegerField(null=True, blank=True)

    # -- LEGALITIES --
    legalities = models.JSONField(default=dict, blank=True, null=True)
    all_parts_raw = models.JSONField(null=True, blank=True)

    # -- PRINT & EDITION --
    artist = models.CharField(max_length=255, null=True, blank=True)
    artist_ids = models.JSONField(null=True, blank=True)
    booster = models.BooleanField(default=True)
    digital = models.BooleanField(default=False)
    promo = models.BooleanField(default=False)
    reprint = models.BooleanField(default=False)
    variation = models.BooleanField(default=False)
    variation_of = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="variations",
        help_text="Base card this card is a variation",
    )
    border_color = models.CharField(max_length=50, null=True, blank=True)
    rarity = models.CharField(max_length=50, null=True, blank=True)
    collector_number = models.CharField(max_length=50, null=True, blank=True)
    set = models.ForeignKey(
        Set, 
        related_name='cards', 
        on_delete=models.CASCADE,
        to_field='id'
    )
    set_name = models.CharField(max_length=255, null=True, blank=True)
    set_type = models.CharField(max_length=50, null=True, blank=True)
    released_at = models.DateField(null=True, blank=True)
    finishes = models.JSONField(default=list, blank=True, null=True)
    foil = models.BooleanField(default=False)
    nonfoil = models.BooleanField(default=False)
    frame = models.CharField(max_length=50, null=True, blank=True)
    frame_effects = models.JSONField(null=True, blank=True)
    games = models.JSONField(default=list, blank=True, null=True)
    promo_types = models.JSONField(null=True, blank=True, db_index=True)
    oversized = models.BooleanField(default=False)
    full_art = models.BooleanField(default=False)
    textless = models.BooleanField(default=False)
    story_spotlight = models.BooleanField(default=False)
    security_stamp = models.CharField(max_length=50, null=True, blank=True)
    flavor_text = models.TextField(blank=True, null=True)   
    watermark = models.CharField(max_length=50, null=True, blank=True)
    
    # -- IMGS & PRICES --
    image_status = models.CharField(default="missing", max_length=50)
    image_uris = models.JSONField(default=dict, null=True, blank=True)
    prices = models.JSONField(default=dict, null=True, blank=True)
    
    # -- URIs --
    uri = models.URLField(null=True, blank=True)
    scryfall_uri = models.URLField(null=True, blank=True)
    rulings_uri = models.URLField(null=True, blank=True)
    prints_search_uri = models.URLField(null=True, blank=True)
    set_uri = models.URLField(null=True, blank=True)
    set_search_uri = models.URLField(null=True, blank=True)
    scryfall_set_uri = models.URLField(null=True, blank=True)
    related_uris = models.JSONField(default=dict, null=True, blank=True)
    purchase_uris = models.JSONField(default=dict, null=True, blank=True)
        
    # -- PREVIEW --
    preview = models.JSONField(null=True, blank=True)
    
    # -- PARTNER --
    has_partner = models.BooleanField(default=False, db_index=True)
    partner_type = models.CharField(
        max_length=50,
        choices=PartnerKeyword.choices, 
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_sync = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['set__released_at', 'set__code', 'collector_number', 'name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['set', 'collector_number']),
        ]

    def __str__(self):
        return self.name
    
    @property
    def is_double_faced(self):
        # Usamos el related_name 'faces' que definiste en CardFace
        return self.faces.count() == 2

    def get_image_url(self):
        """
        Retorna la URL de imagen más apropiada, manejando cartas de una cara, 
        doble cara y casos donde no hay imagen.
        """
        size = 'large'
        # 1. Intentar obtener de la carta principal (Single-faced)
        if self.image_uris and isinstance(self.image_uris, dict):
            # Intentamos el tamaño solicitado, si no, normal, si no, small
            return self.image_uris.get(size) or self.image_uris.get('normal') or self.image_uris.get('small')

        # 2. Si no tiene image_uris, es probable que sea Double-faced
        # Usamos .all() y el primer índice para evitar múltiples hits a la DB si ya están prefetched
        first_face = self.faces.all()[:1] 
        if first_face:
            face = first_face[0]
            if face.image_uris and isinstance(face.image_uris, dict):
                return face.image_uris.get(size) or face.image_uris.get('normal') or face.image_uris.get('small')

        # 3. Imagen por defecto (Reverso de carta Magic oficial de Scryfall)
        return "https://cards.scryfall.io/card_back.png"
    
    def get_full_mana_cost(self):
        if not self.is_double_faced:
            return self.mana_cost or ""
        
        costs = [face.mana_cost for face in self.faces.all() if face.mana_cost]
        return " // ".join(costs)


class CardFace(models.Model):
    # --- CARD IDS ---
    card = models.ForeignKey(
        Card, 
        related_name='faces', 
        on_delete=models.CASCADE
    )    
    object = models.CharField(max_length=50, default="card_face")
    oracle_id = models.UUIDField(null=True, blank=True)
    
    # -- DATA --
    name = models.CharField(max_length=255)
    printed_name = models.CharField(max_length=255, null=True, blank=True)
    layout = models.CharField(max_length=50, null=True, blank=True)
    mana_cost = models.CharField(max_length=100, blank=True, null=True)
    cmc = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    oracle_text = models.TextField(null=True, blank=True)
    printed_text = models.TextField(null=True, blank=True)
    produced_mana = models.JSONField(
        default=list,
        blank=True,
        help_text="Mana produced by this specific face"
    )
    type_line = models.CharField(max_length=255, blank=True, null=True)
    printed_type_line = models.CharField(max_length=255, null=True, blank=True)
    supertypes = models.JSONField(default=list)
    types= models.JSONField(default=list)
    subtypes = models.JSONField(default=list)
    power = models.CharField(max_length=10, blank=True, null=True)
    toughness = models.CharField(max_length=10, blank=True, null=True)
    loyalty = models.CharField(max_length=10, blank=True, null=True)
    defense = models.CharField(max_length=10, blank=True, null=True)
    colors = models.JSONField(default=list, null=True, blank=True)
    color_indicator = models.JSONField(default=list, null=True, blank=True)
    color_identity = models.JSONField(default=list, db_index=True)
    attraction_lights = models.JSONField(null=True, blank=True)

    # -- PRINT & EDITION --
    artist = models.CharField(max_length=255, blank=True, null=True)
    artist_ids = models.UUIDField(blank=True, null=True)
    illustration_id = models.UUIDField(blank=True, null=True)
    flavor_text = models.TextField(blank=True, null=True)   
    watermark = models.CharField(max_length=50, blank=True, null=True)
    
    # -- IMGS & PRICES --
    image_uris = models.JSONField(default=dict, null=True, blank=True) 

    # -- METADATA --
    face_index = models.PositiveSmallIntegerField(
        default=0,
        help_text="Order of the face on the card"
    )
    is_front = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.card.name} - {self.name}"
    
    @property
    def full_type(self):
        prefix = ' '.join(self.supertype + self.cardtype)
        return f"{prefix} — {' '.join(self.subtype)}" if self.subtype else prefix

 
class RelatedCard(models.Model):
    parent = models.ForeignKey(
        Card,
        related_name="related_cards",
        on_delete=models.CASCADE
    )

    # Identidad externa (Scryfall)
    scryfall_id = models.UUIDField(
        null=True,
        editable=False,
        db_index=True
    )

    # Resolución interna (opcional)
    related = models.ForeignKey(
        Card,
        null=True,
        blank=True,
        related_name="reverse_related_cards",
        on_delete=models.SET_NULL,
    )

    object = models.CharField(max_length=50, default="related_card")

    component = models.CharField(
        max_length=50,
        choices=RelationTypes.choices,
        null=True,
        blank=True
    )

    relation_type = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="partner, partner_with, background, friends_forever, etc",
    )

    name = models.CharField(max_length=255)
    type_line = models.CharField(max_length=255)
    uri = models.URLField()

    def __str__(self):
        return f"{self.name} ({self.component})"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["parent", "scryfall_id", "component"],
                name="unique_related_card_per_parent"
            )
        ]


# -- RULINGS --
class Ruling(models.Model):
    oracle_id = models.UUIDField(db_index=True, null=True, blank=True)
    # Relacionamos con Card usando el oracle_id como nexo lógico
    card = models.ForeignKey(
        Card, 
        on_delete=models.CASCADE, 
        related_name='rulings'
    )
    source = models.CharField(max_length=20) 
    published_at = models.DateField()
    comment = models.TextField()

    class Meta:
        verbose_name = "Ruling"
        verbose_name_plural = "Rulings"
        unique_together = ('oracle_id', 'published_at', 'comment')

    def __str__(self):
        return f"Ruling for {self.card.name} ({self.published_at})"
    
    
    
