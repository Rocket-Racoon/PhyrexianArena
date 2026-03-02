from django.core.management.base import BaseCommand
from apps.blind_eternities.services import ScryfallSyncService

class Command(BaseCommand):
    help = 'Sync Creature types catalog from Scryfall API'
    def handle(self, *args, **options):
        self.stdout.write('Sync Creature Catalogs ...')
        
        try:
            type_count = ScryfallSyncService.sync_creature_types()
            if type_count > 0:
                self.stdout.write(self.style.SUCCESS(f'✅ {type_count} new creature types added.'))
            else:
                self.stdout.write(self.style.WARNING('ℹ️ No new types.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Sync Error: {str(e)}'))