import re, requests
from django.conf import settings
from django.db import transaction
from .models import CreatureType, Set
from config.constants import SetTypes

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
    

    @classmethod
    @transaction.atomic
    def sync_all_sets(cls):
        url = f"{cls.API_URL}/sets"
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json().get('data', [])
        
        # PATTERNS
        heroes_pattern = re.compile(r'^PH\d+$')
        un_sets = ['UGL', 'UNH', 'UST', 'UND']
        
        for dset in data:
            set_code = dset['code'].upper()
            set_obj = Set.objects.filter(code=set_code).first()
            set_name = dset['name']
            
            # Categorization Logic
            if set_code in un_sets:
                final_set_type = SetTypes.UNSET
            
            if "Jumpstart" in set_name:
                final_set_type = SetTypes.JUMPSTART
            elif "Front Cards" in set_name:
                final_set_type = SetTypes.FRONTCARDS
            elif heroes_pattern.match(set_code):
                final_set_type = SetTypes.HEROES 
            elif "Art Series" in set_name:
                final_set_type = SetTypes.ART
            elif "Scene Box" in set_name:
                final_set_type = SetTypes.SCENE
            else:
                final_set_type = dset['set_type']
            
            defaults = {
                'mtgo_code' : dset.get('mtgo_code'),
                'arena_code' : dset.get('arena_code'),
                'tcgplayer_id' : dset.get('tcgplayer_id'),
                'name': dset['name'],
                'set_type': final_set_type,
                'released_at': dset.get('released_at'),
                'block_code': dset.get('block_code'),
                'block': dset.get('block'),
                'parent_set_code': dset.get('parent_set_code'),
                'card_count': dset['card_count'],
                'printed_size': dset.get('printed_size'),
                'digital': dset.get('digital', False),
                'foil_only': dset.get('foil_only', False),
                'nonfoil_only': dset.get('nonfoil_only', False),
                'scryfall_uri': dset['scryfall_uri'],
                'uri': dset['uri'],
                'icon_svg_uri': dset.get('icon_svg_uri'),
                'search_uri': dset.get('search_uri'),
            }
            
            if set_obj and set_obj.card_count != defaults['card_count']:
                for key, value in defaults.items():
                    setattr(set_obj, key, value)
                set_obj.save()
                continue
            else:
                Set.objects.create(
                    id=dset['id'],
                    object = dset['object'],
                    code=set_code,
                    **defaults
                )
                
        return len(data)