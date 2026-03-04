from django.core.management.base import BaseCommand
from django.db import transaction
from apps.blind_eternities.models import Card, CardFace, RelatedCard, Set

class Command(BaseCommand):
    help = 'Purga de forma segura y eficiente todas las cartas, caras y relaciones.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='También elimina el catálogo de Sets (colecciones)',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('🧬 Iniciando purga del Multiverso...'))

        # 1. Contar registros iniciales
        total_cards = Card.objects.count()
        # if total_cards == 0:
        #     self.stdout.write(self.style.SUCCESS('La Arena ya está vacía. No hay nada que purgar.'))
        #     return

        # 2. Borrado por lotes (Evita el error de "too many SQL variables")
        batch_size = 500
        processed = 0

        try:
            with transaction.atomic():
                while Card.objects.count() > 0:
                    # Obtenemos un lote de IDs
                    ids = Card.objects.values_list('pk', flat=True)[:batch_size]
                    # Borramos el lote (esto dispara el CASCADE a CardFace y RelatedCard)
                    Card.objects.filter(pk__in=list(ids)).delete()
                    
                    processed += len(ids)
                    self.stdout.write(f'--- Asimilados {processed}/{total_cards} registros...')

            self.stdout.write(self.style.SUCCESS(f'✅ Éxito: {total_cards} cartas y sus componentes han sido eliminados.'))

            # 3. Opción para borrar Sets
            if options['all']:
                set_count = Set.objects.count()
                Set.objects.all().delete()
                self.stdout.write(self.style.SUCCESS(f'✅ {set_count} Sets eliminados del archivo.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error durante la purga: {str(e)}'))