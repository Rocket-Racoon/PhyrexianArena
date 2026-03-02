import requests
from django.conf import settings
from django.db import transaction
from .models import CreatureType

class ScryfallSyncService:
    API_URL = getattr(settings, 'SCRYFALL_API_URL')
    DELAY = getattr(settings, 'SCRYFALL_RATE_LIMIT_DELAY')
    
    @classmethod
    @transaction.atomic
    def sync_creature_types(cls):
        url = f"{cls.API_URL}/catalog/creature-types"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        types_list = response.json().get('data', [])
        existing = set(CreatureType.objects.values_list('name', flat=True))
        new_entries = [CreatureType(name=t) for t in types_list if t not in existing]
        
        if new_entries:
            CreatureType.objects.bulk_create(new_entries)
        return len(new_entries)