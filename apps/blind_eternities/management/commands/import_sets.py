from django.core.management.base import BaseCommand
from apps.blind_eternities.services import ScryfallSyncService

class Command(BaseCommand):
    help = 'Sync Sets catalog from Scryfall API'
    def handle(self, *args, **options):
        self.stdout.write('Sync Set Catalogs ...')
        
        try:
            set_count = ScryfallSyncService.sync_all_sets()
            if set_count > 0:
                self.stdout.write(self.style.SUCCESS(f'✅ {set_count} new sets added.'))
            else:
                self.stdout.write(self.style.WARNING('ℹ️ No new sets.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Sync Error: {str(e)}'))