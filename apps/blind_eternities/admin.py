from django.contrib import admin
from django.db.models import Count
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from .models import Set, Card


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