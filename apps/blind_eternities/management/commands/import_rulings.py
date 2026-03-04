import json
from django.core.management.base import BaseCommand
from blind_eternities.models import Card, Ruling

class Command(BaseCommand):
    help = 'Import Card rulings'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to .json rulings file')

    def handle(self, *args, **options):
        file_path = options['json_file']

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error al leer el archivo: {e}"))
            return

        total = len(data)
        created_count = 0
        skipped_count = 0

        self.stdout.write(f"Iniciando importación de {total} rulings...")

        for item in data:
            oracle_id = item.get('oracle_id')
            card = Card.objects.filter(oracle_id=oracle_id).first()
            
            if not card:
                skipped_count += 1
                continue

            obj, created = Ruling.objects.update_or_create(
                oracle_id=oracle_id,
                published_at=item.get('published_at'),
                comment=item.get('comment'),
                defaults={
                    'card': card,
                    'source': item.get('source', 'wotc')
                }
            )

            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Proceso finalizado: {created_count} creados, {skipped_count} saltados por falta de carta."
        ))