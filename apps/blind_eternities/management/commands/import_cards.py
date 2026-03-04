import json, re
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from apps.blind_eternities.models import Card, CardFace, RelatedCard, Set
from config.constants import PartnerKeyword

class Command(BaseCommand):
    help = "Importa cartas desde un archivo JSON de Scryfall"

    def add_arguments(self, parser):
        parser.add_argument(
            "json_path",
            type=str,
            help="Ruta al archivo JSON con cartas de Scryfall",
        )
    
    
    def extract_commander_flags(self, oracle_text, type_line, legalities: dict):
        oracle_text = (oracle_text or "").lower()
        type_line = (type_line or "").lower()
        # --- Is a commander card ---
        is_legendary_creature = (
            "legendary" in type_line and "creature" in type_line
        )
        is_legendary_vehicle = (
            "legendary" in type_line and "vehicle" in type_line
        )
        # --- Can be commander ---
        can_be_commander = "can be your commander" in oracle_text.lower()
        # --- Is Commander --
        is_commander = is_legendary_creature or is_legendary_vehicle or can_be_commander
        # --- Is banned in commander ---
        is_banned = legalities.get("commander") == "banned"
        is_restricted = legalities.get("vintage") == "restricted"
        # --- Multiple copies logic ---
        can_have_multiple = False
        max_copies = 1
        any_number_pattern = re.search(
            r"a deck can have any number of cards named",
            oracle_text,
            re.IGNORECASE,
        )
        up_to_pattern = re.search(
            r"a deck can have up to (\d+) cards named",
            oracle_text,
            re.IGNORECASE,
        )
        if any_number_pattern:
            can_have_multiple = True
            max_copies = 999
        elif up_to_pattern:
            can_have_multiple = True
            max_copies = int(up_to_pattern.group(1))
        return {
            "can_be_commander": is_commander,
            "is_banned": is_banned,
            "is_restricted": is_restricted,
            "can_have_multiple_copies": can_have_multiple,
            "max_copies_in_deck": max_copies,
            "banned_as_companion": False,
        }


    def extract_partner_flags(self, oracle_text, type_line):
        oracle = (oracle_text or "").lower()
        type_line = type_line or ""
        
        if PartnerKeyword.PARTNER.lower() in oracle:
            return PartnerKeyword.PARTNER
        if PartnerKeyword.PARTNER_WITH.lower() in oracle:
            return PartnerKeyword.PARTNER_WITH
        if PartnerKeyword.FRIENDS_FOREVER.lower() in oracle:
            return PartnerKeyword.FRIENDS_FOREVER
        if PartnerKeyword.DOCTORS_COMPANION.lower() in oracle:
            return PartnerKeyword.DOCTORS_COMPANION
        if PartnerKeyword.BACKGROUND.lower() in oracle:
            return PartnerKeyword.BACKGROUND
        if PartnerKeyword.CHARACTER_SELECT.lower() in oracle:
            return PartnerKeyword.CHARACTER_SELECT
        return None

    @transaction.atomic
    def handle(self, *args, **options):
        json_path = Path(options["json_path"])

        if not json_path.exists():
            raise CommandError(f"Archivo no encontrado: {json_path}")

        self.stdout.write(self.style.NOTICE(f"Leyendo {json_path}"))

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            raise CommandError("El JSON debe ser un array de cartas")

        created = 0
        updated = 0
        skipped = 0
        total = len(data)

        for card_data in data:
            # card_id = card_data.get("oracle_id")
            
            # if not card_id:
            #     self.stdout.write(
            #         self.style.WARNING(
            #             f"Saltando carta {card.name} no tiene oracle_id."
            #         )
            #     )
            #     continue
            
            # if Card.objects.filter(oracle_id=card_id).exists():
            #    skipped += 1
            #    continue
            
            card, was_created = self.upsert_card(card_data)
            
            if was_created:
                created += 1
            else:
                updated += 1
                
            if (created + updated) % 100 == 0:
                percentage = ((created + updated )/ total)*100 
                print(f" Procesadas {created + updated}/{total} cartas... { percentage:.2f } %")

        self.stdout.write(
            self.style.SUCCESS(
                f"Importación completada. Creadas: {created}, Actualizadas: {updated}, Skipped: {skipped}"
            )
        )


    def upsert_card(self, c):
        flags = self.extract_commander_flags(
            oracle_text = c.get("oracle_text") or " ".join(
                face.get("oracle_text", "") for face in c.get("card_faces", [])
            ),
            type_line = c.get("type_line"),
            legalities=c.get("legalities", {}),
        )
        
        partner_key = self.extract_partner_flags(
            oracle_text = c.get("oracle_text") or " ".join(
                face.get("oracle_text", "") for face in c.get("card_faces", [])
            ),
            type_line = c.get("type_line"),
        )
        
        set_code = c.get("set").upper()
        try:
            set_instance = Set.objects.get(code=set_code)
        except Set.DoesNotExist:
            self.stdout.write(self.style.WARNING(f"⚠️ Set {set_code} no encontrado en el catálogo. Creando temporal..."))
            set_instance = Set.objects.create(
                code=set_code,
                name=c.get("set_name", set_code)
            )

        raw_cmc = c.get("cmc", 0)
        try:
            clean_cmc = round(float(raw_cmc), 1) if raw_cmc is not None else 0
        except (ValueError, TypeError):
            clean_cmc = 0
            
        variation_of_id = c.get("variation_of")
        variation_of_card = None

        if variation_of_id:
            variation_of_card = Card.objects.filter(id=variation_of_id).first()
        
        card, created = Card.objects.update_or_create(
            id=c["id"],
            defaults={
                # --- CORE IDS ---
                "oracle_id": c.get("oracle_id"),
                "arena_id": c.get("arena_id"),
                "mtgo_id": c.get("mtgo_id"),
                "mtgo_foil_id": c.get("mtgo_foil_id"),
                "multiverse_ids": c.get("multiverse_ids"),
                "resource_id": c.get("resource_id"),
                "tcgplayer_id": c.get("tcgplayer_id"),
                "tcgplayer_etched_id": c.get("tcgplayer_etched_id"),
                "cardmarket_id": c.get("cardmarket_id"),
                # --- METADATA ---
                "lang": c.get("lang"),
                "object": c.get("object", "card"),
                "layout": c.get("layout"),
                "edhrec_rank": c.get("edhrec_rank"),
                "penny_rank": c.get("penny_rank"),
                # --- GAMEPLAY DATA ---
                "name": c.get("name"),
                "printed_name": c.get("printed_name"),
                "mana_cost": c.get("mana_cost"),
                "cmc": clean_cmc,
                "type_line": c.get("type_line"),
                "oracle_text": c.get("oracle_text"),
                "flavor_text": c.get("flavor_text"),
                "keywords": c.get("keywords", []),
                "power": c.get("power"),
                "toughness": c.get("toughness"),
                "loyalty": c.get("loyalty"),
                "defense": c.get("defense"),
                "attraction_lights": c.get("attraction_lights", []),
                "colors": c.get("colors"),
                "color_identity": c.get("color_identity", []),
                "color_indicator": c.get("color_indicator"),
                "produced_mana": c.get("produced_mana"),
                # --- VANGUARD ---
                "hand_modifier": c.get("hand_modifier"),
                "life_modifier": c.get("life_modifier"),                
                # --- LEGALITIES
                "legalities": c.get("legalities", {}),
                "reserved": c.get("reserved", False),
                "game_changer": c.get("game_changer"),
                # --- VERSION ---
                "artist": c.get("artist"),
                "artist_ids": c.get("artist_ids"),
                "booster": c.get("booster", True),
                "digital": c.get("digital", False),
                "promo": c.get("promo", False),
                "reprint": c.get("reprint", False),
                "variation": c.get("variation", False),
                "variation_of": variation_of_card,                
                "border_color": c.get("border_color"),
                "rarity": c.get("rarity"),
                "collector_number": c.get("collector_number"),
                "set": set_instance,
                "set_name": c.get("set_name"),
                "set_type": c.get("set_type"),
                "released_at": c.get("released_at"),
                "finishes": c.get("finishes", []),
                "frame_effects": c.get("frame_effects"),
                "games": c.get("games", []),
                "promo_types": c.get("promo_types"),
                "frame": c.get("frame"),
                "foil": c.get("foil", False),
                "nonfoil": c.get("nonfoil", False),
                "oversized": c.get("oversized", False),
                "full_art": c.get("full_art", False),
                "textless": c.get("textless", False),
                "story_spotlight": c.get("story_spotlight", False),
                # --- Print ---
                "printed_name": c.get("printed_name"),
                "printed_text": c.get("printed_text"),
                "printed_type_line": c.get("printed_type_line"),
                "security_stamp": c.get("security_stamp"),
                "watermark": c.get("watermark"),
                # --- Images & Prices ---
                "image_status": c.get("image_status"),
                "image_uris": c.get("image_uris"),
                "prices": c.get("prices"),
                # --- URIs ---
                "uri": c.get("uri"),
                "scryfall_uri": c.get("scryfall_uri"),
                "rulings_uri": c.get("rulings_uri"),
                "prints_search_uri": c.get("prints_search_uri"),
                "set_uri": c.get("set_uri"),
                "set_search_uri": c.get("set_search_uri"),
                "scryfall_set_uri": c.get("scryfall_set_uri"),
                "related_uris": c.get("related_uris"),
                "purchase_uris": c.get("purchase_uris"),
                # --- Preview ---
                "preview": c.get("preview"),
                # --- Commander / Deck rules ---
                "can_be_commander": flags["can_be_commander"],
                "is_banned": flags["is_banned"],
                "can_have_multiple_copies": flags["can_have_multiple_copies"],
                "max_copies_in_deck": flags["max_copies_in_deck"],
                "banned_as_companion": flags["banned_as_companion"],
                # -- Partner --
                "has_partner": bool(partner_key),
                "partner_type": partner_key,
                # --- Variety info ---
                "is_token": c.get("layout") == "token",
                "is_emblem": c.get("layout") == "emblem",
                "is_restricted": flags["is_restricted"],
                "available_languages": [c.get("lang")] if c.get("lang") else [],
            },
        )

        # --- Card Faces ---
        if c.get("card_faces"):
            card.faces.all().delete()

            for i, face in enumerate(c["card_faces"]):
                CardFace.objects.create(
                    card=card,
                    object=face.get("object", "card_face"),
                    name=face.get("name"),
                    layout=face.get("layout"),
                    mana_cost=face.get("mana_cost", ""),
                    cmc=face.get("cmc"),
                    oracle_id=face.get("oracle_id"),
                    oracle_text=face.get("oracle_text"),
                    type_line=face.get("type_line"),
                    supertypes=face.get("supertypes", []),
                    types=face.get("types", []),
                    subtypes=face.get("subtypes", []),
                    power=face.get("power"),
                    toughness=face.get("toughness"),
                    loyalty=face.get("loyalty"),
                    defense=face.get("defense"),
                    attraction_lights=face.get("attraction_lights"),
                    produced_mana=face.get("produced_mana", []),
                    colors=face.get("colors"),
                    color_indicator=face.get("color_indicator"),
                    color_identity=face.get("color_identity", []),
                    artist=face.get("artist"),
                    artist_ids=(
                        face.get("artist_ids")[0]
                        if face.get("artist_ids")
                        else None
                    ),
                    illustration_id=face.get("illustration_id"),
                    flavor_text=face.get("flavor_text"),
                    watermark=face.get("watermark"),
                    image_uris=face.get("image_uris"),
                    printed_name=face.get("printed_name"),
                    printed_text=face.get("printed_text"),
                    printed_type_line=face.get("printed_type_line"),
                    face_index=i,
                    is_front=(i == 0),
                )

        # --- Related Cards ---
        if c.get("all_parts"):
            card.related_cards.all().delete()

            for part in c["all_parts"]:
                RelatedCard.objects.create(
                    parent=card,
                    scryfall_id=part.get("id"),
                    object=part.get("object", "related_card"),
                    component=part.get("component"),
                    name=part.get("name"),
                    type_line=part.get("type_line"),
                    uri=part.get("uri"),
                )

        if partner_key:
            RelatedCard.objects.filter(
                parent=card,
                component="combo_piece"
            ).update(relation_type=partner_key)

        return card, created

