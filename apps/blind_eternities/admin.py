from django.contrib import admin
from django.db.models import Count
from django.template.loader import render_to_string
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Set, Card, CardFace, RelatedCard, Ruling


# -- SET --

@admin.action(description='Set Commander Status: True')
def mark_commanders(modeladmin, request, queryset):
    queryset.update(has_commanders=True)

@admin.action(description='Set Commander Status: False')
def unmark_commanders(modeladmin, request, queryset):
    queryset.update(has_commanders=False)


@admin.register(Set)
class SetAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'parent_set_code', 'has_commanders', 'set_type', 'released_at', 'card_count', 'digital')
    readonly_fields = ('set_stats_dashboard',)
    actions = [mark_commanders, unmark_commanders]
    list_editable = ('has_commanders', 'card_count')

    def set_stats_dashboard(self, obj):
        cards = Card.objects.filter(set=obj)
        if not cards.exists():
            return "Pendiente de importación."
        
        # Agregación de Maná y cálculo de porcentaje para la altura de las barras
        mana_data = cards.values('cmc').annotate(total=Count('id')).order_by('cmc')
        
        if not mana_data:
            return "Sin datos de maná disponibles."
 
        # Encontramos el valor máximo para escalar las barras (Eje Y)
        max_cards = max([m['total'] for m in mana_data]) if mana_data else 1
 
        # Construimos la curva sin límites
        mana_curve = []
        for m in mana_data:
            # Forzamos el cálculo a float y redondeamos para el CSS
            percentage = round((m['total'] / max_cards) * 100, 2)
            mana_curve.append({
                'label': str(int(m['cmc'])),
                'total': m['total'],
                'percentage': percentage
            })

        # Conteo de colores y valor
        color_counts = {'W': 0, 'U': 0, 'B': 0, 'R': 0, 'G': 0}
        total_value = 0.0
        for card in cards:
            for color in card.color_identity:
                if color in color_counts: color_counts[color] += 1
            
            usd_price = card.prices.get('usd')
            if usd_price: total_value += float(usd_price)
  
        # Contexto para el template
        context = {
            'mana_curve': mana_curve,
            'color_counts': color_counts,
            'commander_count': cards.filter(can_be_commander=True).count(),
            'total_value': total_value,
        }

        # Renderizamos el archivo HTML externo
        html = render_to_string('admin/blind_eternities/set_stats_dashboard.html', context)
        return mark_safe(html)

    set_stats_dashboard.short_description = "Estadísticas del Set"

# -- CARD --
@admin.action(description="Ban Selected Card(s)")
def make_banned(modeladmin, request, queryset):
    queryset.update(is_banned=True)

@admin.action(description="Un-Ban Selected Card(s)")
def remove_banned(modeladmin, request, queryset):
    queryset.update(is_banned=False)

@admin.action(description="Mark as Restricted Selected Card(s)")
def make_restricted(modeladmin, request, queryset):
    queryset.update(is_restricted=True)

@admin.action(description="Unmark as Restricted Selected Card(s)")
def remove_restricted(modeladmin, request, queryset):
    queryset.update(is_restricted=False)

@admin.action(description="Mark as GC Selected Card(s)")
def make_gamechanger(modeladmin, request, queryset):
    queryset.update(game_changer=True)

@admin.action(description="Unmark as GC Selected Card(s)")
def remove_gamechanger(modeladmin, request, queryset):
    queryset.update(game_changer=False)


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('collector_number','name', 'get_set_name', 'mana_cost', 'colors', 'type_line', 
                    'rarity', 'created_at', 'updated_at', 'game_changer', 'is_banned', 
                    'is_restricted') 
    actions = [make_banned, remove_banned, make_gamechanger, remove_gamechanger, 
               make_restricted, remove_restricted]

    list_filter = ('set', 'rarity', 'promo', 'reprint', 'game_changer', 
                   'is_banned', 'is_restricted')
    
    search_fields = ('name', 'type_line', 'oracle_id', 'keywords', 'set_name')
    fieldsets = (
        ('Información Básica', {
            'fields': ('name', 'set', 'mana_cost', 'type_line', 'rarity')
        }),
        ('Atributos de Juego', {
            'fields': ('cmc', 'colors', 'color_identity', 'keywords', 'oracle_id', 'oracle_text', 'flavor_text')
        }),
        ('Estado y Colección', {
            'fields': ('is_banned', 'game_changer', 'can_be_commander', 'promo', 'reprint')
        }),
        ('Metadata de Scryfall (JSON)', {
            'classes': ('collapse',), 
            'fields': ('image_uris', 'prices', 'legalities', 'purchase_uris', 'related_uris')
        }),
    )
    list_select_related = ('set',)
    
    def get_set_name(self, obj):
        silver_filter = "filter: grayscale(1) brightness(1.2) contrast(1.1);"
        if obj.set and obj.set.icon_svg_uri:
            return format_html(
                '<img src="{}" style="width:20px; height:20px; margin-right:8px; vertical-align:middle; {}"> {}',
                obj.set.icon_svg_uri,
                silver_filter,
                obj.set.code
            )
        return obj.set.name if obj.set else "-"

    get_set_name.short_description = 'Set'
    

@admin.register(CardFace)
class CardFaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'mana_cost', 'type_line', 'color_identity', 'layout')
    search_fields = ('name', 'type_line')


class CardFaceInline(admin.StackedInline):
    model = CardFace
    extra = 0
    readonly_fields = ('full_type_line',)
    fieldsets = (
        (None, {
            'fields': (('name', 'mana_cost', 'cmc'),)
        }),
        ('Card Attributes', {
            'fields': (('power', 'toughness', 'loyalty', 'defense'),)
        }),
        ('Typal', {
            'fields': ('supertypes', 'card_types', 'subtypes', 'full_type_line')
        }),
        ('Content', {
            'fields': ('oracle_text', 'image_uri')
        }),
    )


@admin.register(RelatedCard)
class RelatedCardAdmin(admin.ModelAdmin):
    list_display = ('name','type_line')
    
@admin.register(Ruling)
class RulingAdmin(admin.ModelAdmin):
    list_display = ('card','published_at', 'source')