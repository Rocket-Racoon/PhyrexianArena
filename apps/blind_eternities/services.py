import json, re, requests, time
from django.conf import settings
from django.db import transaction
from .models import CreatureType, Set, Card, CardFace
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

        for dset in data:
            set_code = dset.get('code', '').upper()
            block_code = dset.get('block_code', '').upper()
            pset_code = dset.get('parent_set_code', '').upper()

            final_set_type = (cls._set_category_set(dset['name'], set_code) or dset['set_type'])

            defaults = {
                'mtgo_code': dset.get('mtgo_code'),
                'arena_code': dset.get('arena_code'),
                'tcgplayer_id': dset.get('tcgplayer_id'),
                'name': dset['name'],
                'set_type': final_set_type,
                'released_at': dset.get('released_at'),
                'block_code': block_code,
                'block': dset.get('block'),
                'parent_set_code': pset_code,
                'card_count': dset['card_count'],
                'printed_size': dset.get('printed_size'),
                'digital': dset.get('digital', False),
                'foil_only': dset.get('foil_only', False),
                'nonfoil_only': dset.get('nonfoil_only', False),
                'scryfall_uri': dset['scryfall_uri'],
                'uri': dset['uri'],
                'icon_svg_uri': dset.get('icon_svg_uri'),
                'search_uri': dset.get('search_uri'),
                'object': dset.get('object', 'set'),
            }
            
            defaults['id'] = dset['id']
            defaults['object'] = dset.get('object', 'set')

            obj, created = Set.objects.update_or_create(
                id=dset['id'],
                code=set_code,
                defaults=defaults
            )

            status = "Creado" if created else "Actualizado"
            print(f"[{status}] {set_code} - {dset['name']}")

        return len(data)
    

    @classmethod
    @transaction.atomic
    def process_card_data(cls, data):
        set_data = data['set'].upper()
        set_obj = Set.objects.filter(code= set_data).first()
        if not set_obj:
            set_obj = cls._fetch_single_set(set_data)
        faces_data = data.get('card_faces', [])
        primary_face = faces_data[0] if faces_data else data
        
        # -- DATA EXTRACTION --
        mana_cost = data.get('mana_cost') or primary_face.get('mana_cost', '')
        type_line = data.get('type_line') or primary_face.get('type_line', '')
        oracle_text = data.get('oracle_text') or primary_face.get('oracle_text', '')
        image_uris = data.get('image_uris') or primary_face.get('image_uris', {})
        
        if not data.get('oracle_text') and faces_data:
            oracle_text = "\n//\n".join(
                [f.get('oracle_text', '') for f in faces_data if f.get('oracle_text')]
            )
            
        card, _ = Card.objects.update_or_create(
            id=data['id'],
            defaults={
                # IDs
                'oracle_id': data.get('oracle_id'),
                'arena_id': data.get('arena_id'),
                'mtgo_id': data.get('mtgo_id'),
                'mtgo_foil_id': data.get('mtgo_foil_id'),
                'multiverse_ids': data.get('multiverse_id'),
                'resource_id': data.get('resource_id'),
                'tcgplayer_id': data.get('tcgplayer_id'),
                'tcgplayer_etched_id': data.get('tcgplayer_etched_id'),
                'cardmarket_id': data.get('cardmarket_id'),
                # METADATA
                'object': data.get('object'),
                'lang': data.get('lang', 'en'),
                'layout': data.get('layout'),
                # DATA
                'name': data['name'],
                'printed_name': data.get('printed_name'),
                'oracle_text': oracle_text,
                'printed_text': data.get('printed_text'),
                'type_line': type_line,      
                'printed_type_line': data.get('printed_type_line'),
                'keywords': data.get('keywords', []),
                'cmc': data.get('cmc', 0.0),
                'mana_cost': mana_cost,
                'power': data.get(''),
                'toughness': data.get(''),
                'loyalty': data.get(''),
                'defense': data.get(''),
                'attraction_lights': data.get(''),
                'colors': data.get('colors'),
                'color_identity': data.get('color_identity', []),
                'color_indicator': data.get('color_inicator'),
                'produced_mana': data.get('produced_mana'),
                'reserved': data.get('reserved'),
                'game_changer': data.get('game_changer'),
                'flavor_name': data.get('flavor_name'),
                'available_languages': data.get('available_languages'),
                # VANGUARD
                'hand_modifier': data.get('hand_modifier'),
                'life_modifier': data.get('life_modifier'),
                # RANK DATA
                'edhrec_rank': data.get('edhrec_rank'),
                'penny_rank': data.get('penny_rank'),
                # LEGALITIES
                'legalities': data.get('legalities', {}),
                'all_parts_raw': data.get('all_parts_raw'),
                # PRINTS & EDITIONS
                'artist': primary_face.get('artist'),
                'artist_ids': primary_face.get('artist_ids'),
                'booster': data.get(''),
                'promo': data.get('promo', False),
                'reprint': data.get('reprint', False),
                'variation': data.get('variation'),
                'variation_of': data.get('variation_of'),
                'border_color': data.get('border_color'),
                'rarity': data.get('rarity'),
                'collector_number': data.get('collector_number'),
                'set': set_obj,
                'set_name': data.get('set_name'),
                'set_type': data.get('set_type'),
                'released_at': data.get('released_at'),
                'finishes': data.get('finishes'),
                'foil': data.get('foil'),
                'nonfoil': data.get('nonfoil'),
                'frame': data.get('frame'),
                'frame_effects': data.get(''),
                'games': data.get('games'),
                'promo_types': data.get('promo_types'),
                'oversized': data.get('oversized'),
                'full_art': data.get('full_art'),
                'textless': data.get('textless'),
                'story_spotlight': data.get('story_spotlight'),
                'security_stamp': data.get('security_stamp'),
                'flavor_text': data.get('flavor_text'),
                'watermark': data.get('watermark'),
                # IMGS & PRICES
                'image_status': data.get('image_status'),
                'image_uris': image_uris,
                'prices': data.get('prices', {}),
                # URIS
                'uri': data.get('uri'),
                'scryfall_uri': data.get('scryfall_uri'),
                'rulings_uri': data.get('rulings_uri'),
                'prints_search_uri': data.get('prints_search_uri'),
                'set_uri': data.get('set_uri'),
                'set_search_uri': data.get('set_search_uri'),
                'scryfall_set_uri': data.get('scryfall_set_uri'),
                'related_uris': data.get('related_uris', {}),
                'purchase_uris': data.get('purchase_uris', {}),
                # PREVIEW
                'preview': data.get(''),
                # PARTNER
                'has_partner': data.get('has_partner'),
                'partner_type': data.get('partner_type'),
            }
        )
        
        cls._process_faces(card, data)
        card.can_have_multiple_copies, card.max_copies_in_deck = cls._proccess_multiple_copies(card)
        
        card.is_banned = cls._check_isbanned(card)
        card.is_token = cls._check_istoken(card)
        card.is_emblem = cls._check_isemblem(card)
        card.can_be_commander = cls._check_commander_legality(card)
        
        card.save()
 
            
            
    # -- PRIVATE METHODS --
    @classmethod
    def _fetch_single_set(cls, set_code):
        """Busca un set específico si no estaba en la DB."""
        time.sleep(cls.DELAY)
        url = f"{cls.BASE_URL}/sets/{set_code}"
        res = requests.get(url)
        if res.status_code == 200:
            dset = res.json()
            set_code = dset['code'].upper()
            final_set_type = (cls._set_category_set(set_name=dset['name'], set_code=dset['code']) or dset['set_type'])
            
            defaults = {
                'mtgo_code' : dset.get('mtgo_code'),
                'arena_code' : dset.get('arena_code'),
                'tcgplayer_id' : dset.get('tcgplayer_id'),
                'name': dset['name'],
                'set_type': final_set_type,
                'released_at': dset.get('released_at'),
                'block_code': dset.get('block_code').upper(),
                'block': dset.get('block'),
                'parent_set_code': dset.get('parent_set_code').upper(),
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
            
            return Set.objects.create(
                id=dset['id'],
                object = dset['object'],
                code=set_code,
                **defaults
            )
        raise ValueError(f"Set {set_code} not found in Scryfall.")


    @classmethod
    def _set_category_set(cls, set_name, set_code):
        if "Front Cards" in set_name:
            return SetTypes.FRONTCARDS
        if re.match(r'^PH\d+$', set_code):
            return SetTypes.HEROES
        if set_code in {'UGL', 'UNH', 'UST', 'UND', 'UNF'}:
            return SetTypes.UNSET
        if "Art Series" in set_name:
            return SetTypes.ART
        if "Scene Box" in set_name:
            return SetTypes.SCENE
        if "Jumpstart" in set_name:
            return SetTypes.JUMPSTART
        return None
    
    
    @classmethod
    def _process_faces(cls, card, data):
        """Maneja la creación de CardFace para cartas simples y complejas."""
        CardFace.objects.filter(card=card).delete()
        
        raw_faces = data.get('card_faces', [data])
        faces_to_create = []

        for f_data in raw_faces:
            supertypes, types, subtypes = cls._parse_type_line(f_data.get('type_line', ''))
            
            face_image = f_data.get('image_uris', card.image_uris)
            
            face = CardFace(
                # IDS
                card=card,
                object = f_data.get('object', ''),
                oracle_id = f_data.get('oracle_id', ''),
                # DATA
                name= f_data.get('name', card.name),
                printed_name = f_data.get('printed_name', ''),
                layout = f_data.get('layout', ''),
                cmc = f_data.get('cmc', ''),
                mana_cost = f_data.get('mana_cost', ''),
                oracle_text = f_data.get('oracle_text', ''),
                printed_text = f_data.get('printed_text', ''),
                produced_mana = f_data.get('produced_mana', ''),
                type_line = f_data.get('type_line', ''),
                supertypes = supertypes,
                types = types,
                subtypes = subtypes,
                power = f_data.get('power'),
                toughness = f_data.get('toughness'),
                loyalty = f_data.get('loyalty'),
                defense = f_data.get('defense'),
                colors = f_data.get('colors', ''),
                color_indicator = f_data.get('color_indicator', ''),
                color_identity = f_data.get('color_identity', ''),
                attraction_lights = f_data.get('attraction_lights', ''),
                # PRINT & EDITION
                artist = f_data.get('artist', card.artist),
                artist_ids = f_data.get('artist_ids', ''),
                illustration_id = f_data.get('illustration_id', ''),
                flavor_text = f_data.get('flavor_text', ''),
                watermark = f_data.get('watermark', ''),
                # IMG & PRICES
                image_uris = face_image, 
                face_index = f_data.get('face_index', ''),
                is_front = f_data.get('is_front', '')
            )
            
            faces_to_create.append(face)
        
        CardFace.objects.bulk_create(faces_to_create)
        
    @staticmethod
    def _check_commander_legality(card):
        """Implementa las reglas de validación de Comandante (RC)."""
        
        for face in card.faces.all():
            # Regla 1: Criatura Legendaria
            if 'Legendary' in face.supertypes and 'Creature' in face.types:
                return True
            # Regla 2: Vehículo Legendario
            if 'Legendary' in face.supertypes and 'Vehicle' in face.subtypes:
                return True
            # Regla 3: Planeswalker con texto explícito
            if 'Planeswalker' in face.types:
                text = (face.oracle_text or "").lower()
                if "can be your commander" in text:
                    return True
        return False
    
    @staticmethod
    def _check_isbanned(card):
        if card.legalities.get('commander') != 'legal':
            return False
    
    @staticmethod
    def _check_istoken(card):
        layout = card.get('layout', '')
        type_line = card.get('type_line', '')
        if layout in ['token', 'double_faced_token'] or "Token" in type_line:
            return True
        return False
    
    
    @staticmethod
    def _check_isemblem(card):
        layout = card.get('layout', '')
        type_line = card.get('type_line', '')
        if layout == 'emblem' or "Emblem" in type_line:
            return True
        return False
    
    
    @staticmethod
    def _proccess_multiple_copies(card):
        number = 1
        
        if hasattr(card, 'type_line') and "Basic" in card.type_line:
            return True, 99
    
        any_number_pattern = re.compile(r"A deck can have any number of cards named", re.IGNORECASE)
        seven_dwarves_pattern = re.compile(r"A deck can have up to seven cards named", re.IGNORECASE)
        nine_nazguls_pattern = re.compile(r"A deck can have up to nine cards named", re.IGNORECASE)
    
        all_texts = []
        if hasattr(card, 'faces') and card.faces.exists():
            for face in card.faces.all():
                if face.oracle_text:
                    all_texts.append(face.oracle_text)
        elif hasattr(card, 'oracle_text') and card.oracle_text:
            all_texts.append(card.oracle_text)
        
        combined_text = " ".join(all_texts)
        
        if any_number_pattern.search(combined_text):
            return True, float('inf')

        if seven_dwarves_pattern.search(combined_text):
            return True, 7
        
        if nine_nazguls_pattern.search(combined_text):
            return True, 9
    
        return False, number