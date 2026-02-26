from django.db import models

# USER RANKS
class UserRank(models.TextChoices):
    GERM        = 'rank_0', 'Germ'
    NEWT        = 'rank_1', 'Newt'
    MINION      = 'rank_2', 'Minion'
    SLEEPER     = 'rank_3', 'Sleeper Agent'
    OVERLORD    = 'rank_4', 'Overlord'
    PRAETOR     = 'rank_5', 'Preaetor'


# Card Parts
class CardPart(models.TextChoices):
    NAME            = 'name', 'Name'
    MANA_COST       = 'mana_cost', 'Mana Cost'
    COLOR           = 'color', 'Color'
    ILLUSTRATION    = 'illustration', 'Illustration'
    INDICATOR       = 'color_indicator', 'Color Indicator'
    TYPELINE        = 'type_line', 'Type Line'
    EXPANSIONSYMBOL = 'expansion_symbol', 'Expansion Symbol'
    TEXTBOX         = 'text_box', 'Text Box'
    POWER_TOUGHNESS = 'power_toughness', 'Power/Toughness'
    LOYALTY         = 'loyalty', 'Loyalty'
    DEFENSE         = 'defense', 'Defense'
    HANDMOD         = 'hand_modifier', 'Hand Modifier'
    LIFEMOD         = 'life_modifier', 'Life Modifier'
    INFORMATION     = 'information', 'Information'


# Card Properties
class CardType(models.TextChoices):
    ARTIFACT        = 'artifact', 'Artifact'
    CREATURE        = 'creature', 'Creature'
    ENCHANTMENT     = 'enchantment', 'Enchantment'
    INSTANT         = 'instant', 'Instant'
    LAND            = 'land', 'Land'
    PLANESWALKER    = 'planeswalker', 'Planeswalker'
    SORCERY         = 'sorcery', 'Sorcery'
    KINDRED         = 'kindred', 'Kindred'
    DUNGEON         = 'dungeon', 'Dungeon'
    BATTLE          = 'battle', 'Battle'
    PLANE           = 'plane', 'Plane'
    PHENOMENON      = 'phenomenon', 'Phenomenon'
    VANGUARD        = 'vanguard', 'Vanguard'
    SCHEME          = 'scheme', 'Scheme'
    CONSPIRACY      = 'conspiracy', 'Conspiracy'
    EMBLEM          = 'emblem', 'Emblem'
    HERO            = 'hero', 'Hero'


class SuperType(models.TextChoices):
    BASIC       = 'Basic', 'Basic'
    ELITE       = 'Elite', 'Elite'
    LEGENDARY   = 'Legendary', 'Legendary'
    ONGOING     = 'Ongoing', 'Ongoing'
    SNOW        = 'Snow', 'Snow'
    TOKEN       = 'Token', 'Token'
    WORLD       = 'World', 'World'


class Color(models.TextChoices):
    WHITE       = 'W', 'White'
    BLUE        = 'U', 'Blue'
    BLACK       = 'B', 'Black'
    RED         = 'R', 'Red'
    GREEN       = 'G', 'Green'
    COLORLESS   = 'C', 'Colorless'


class Rarity(models.TextChoices):
    COMMON      = 'common', 'Common'
    UNCOMMON    = 'uncommon', 'Uncommon'
    RARE        = 'rare', 'Rare'
    MYTHIC      = 'mythic', 'Mythic'
    SPECIAL     = 'special', 'Special'
    BONUS       = 'bonus', 'Bonus'
    TIMESHIFTED = 'timeshifted', 'Timeshifted'


class CardLayout(models.TextChoices):
    NORMAL = 'normal', 'Normal'
    # Spells Only
    SPLIT = 'split', 'Split'
    # Creatures Only
    FLIP = 'flip', 'Flip'
    LEVELER = 'leveler', 'Leveler'
    DOUBLE_FACED_CARD = 'dfc', 'Double-Faced Card'
    TRANSFORM = 'transform', 'Transform'
    MUTATE = 'mutate', 'Mutate'
    PROTOTYPE = 'prototype', 'Prototype'
    # Permanents & Spells
    MODAL_DFC = 'modal_dfc', 'Modal DFC'
    ADVENTURE = 'adventure', 'Adventure'
    MELD = 'meld', 'Meld'
    REVERSIBLE_CARD = 'reversible_card', 'Reversible Card'
    # Enchantment Only
    SAGA = 'saga', 'Saga'
    CLASS = 'class', 'Class'
    CASE = 'case', 'Case'
    # Battles
    BATTLE = 'battle', 'Battle'
    # Un Games
    AUGMENT = 'augment', 'Augment'
    HOST = 'host', 'Host'
    ATTRACTION = 'attraction', 'Attraction'
    # Other
    PLANAR = 'planar', 'Planar'
    SCHEME = 'scheme', 'Scheme'
    VANGUARD = 'vanguard', 'Vanguard'
    # Markers
    TOKEN = 'token', 'Token'
    DOUBLE_FACED_TOKEN = 'double_faced_token', 'Double Faced Token'
    EMBLEM = 'emblem', 'Emblem'
    SUBSTITUTE = 'substitute', 'Substitute Card'
    # Art
    ART_SERIES = 'art_series', 'Art Series'
    

class Watermark(models.TextChoices):
    # Lore
    ABZAN       = "Abzan", "Abzan"
    ATARKA      = "Atarka", "Atarka"
    AZORIUS     = "Azorius", "Azorius"
    BOROS       = "Boros", "Boros"
    BROKERS     = "Brokers", "Brokers"
    CABARETTI   = "Cabaretti", "Cabaretti"
    DESPARK     = "Desparked", "Desparked"
    DIMIR       = "Dimir", "Dimir"
    DROMOKA     = "Dromoka", "Dromoka"
    GOLGARI     = "Golgari", "Golgari"
    GRUUL       = "Gruul", "Gruul"
    IZZET       = "Izzet", "Izzet"
    JESKAI      = "Jeskai", "Jeskai"
    KOLAGHAN    = "Kolaghan", "Kolaghan"
    LOREHOLD    = "Lorehold", "Lorehold"
    MAESTROS    = "Maestros", "Maestros"
    MARDU       = "Mardu", "Mardu"
    MIRRAN      = "Mirran", "Mirran"
    OBSCURA     = "Obscura", "Obscura"
    OJUTAI      = "Ojutai", "Ojutai"
    ORZHOV      = "Orzhov", "Orzhov"
    PHYREXIAN   = "Phyrexian", "Phyrexian"
    PRISMARI    = "Prismari", "Prismari"
    QUANDRIX    = "Quandrix", "Quandrix"
    RAKDOS      = "Rakdos", "Rakdos"
    RIVETEERS   = "Riveteers", "Riveteers"
    SELESNYA    = "Selesnya", "Selesnya"
    SILUMGAR    = "Silumgar", "Silumgar"
    SILVERQUILL = "Silverquill", "Silverquill"
    SIMIC       = "Simic", "Simic"
    SULTAI      = "Sultai", "Sultai"
    TARKIR      = "Tarkir", "Tarkir"
    TEMUR       = "Temur", "Temur"
    WITHERBLOOM = "Witherbloom", "Witherbloom"
    # Game
    CONSPIRACY      = "Conspiracy", "Conspiracy"
    FORTELL         = "Fortell", "Fortell"
    PLANESWALKER    = "Planeswalker", "Planeswalker"
    SET             = "Set", "Set"
    # Un-game
    AGENTSSNEAK         = "Agentsofsneak", "Agents of S.N.E.A.K."
    CROSSBREEDLABS      = "Crossbreed Labs", "Crossbreed Labs"
    GOBLINEXPLOSIONEERS = "Goblin Explosioneers", "Goblin Explosioneers"
    LEAGUEDOOM          = "League of Dastarly Doom", "League of Dastarly Doom"
    ORDERWIDGET         = "Order of the Widget", "Order of the Widget"
    # Universe Beyond
    DND             = "D&D", "D&D"
    TRANSFORMERS    = "Transformers", "Transformers"
    AIRNOMADS       = "Air Nomads", "Air Nomads"
    EARTHKINGDOM    = "Earth Kingdom", "Earth Kingdom"
    FIRENATION      = "Fire Nation", "Fire Nation"
    WATERTRIBE      = "Water Tribe", "Water Tribe"
    # Tournament
    DCI         = "DCI", "DCI"
    GRANDPRIX   = "Grand Prix", "Grand Prix"
    JAPANJR     = "Japan Jr", "Japan Jr"
    JR          = "Junior", "Junior Superseries"
    JRAPC       = "Junior APC", "Junior APC"
    JREU        = "Junior Europe", "Junior Europe"
    PROTOUR     = "Pro Tour", "Pro Tour"
    WOTC        = "WOTC", "WOTC"
    WPN         = "WPN", "WPN" 
    # Promotion
    ARENA       = "Arena", "Arena"
    COLORPIE    = "Colorpie", "Colorpie"
    FLAVOR      = "Flavor", "Flavor"
    FNM         = "FNM", "FNM"
    HEROSPATH   = "Heros Path", "Heros Path"
    JUDGE       = "Judge Academy", "Judge Academy"
    MAGICFEST   = "MagicFest", "MagicFest"
    MPS         = "MPS", "MPS"
    MTG         = "MTG", "MTG"
    MTG10       = "MTG10", "MTG10"
    MTG15       = "MTG15", "MTG15"
    SCOLARSHIP  = "Scholarship", "Scholarship"
    # IPs
    COROCORO    = "CoroCoro", "CoroCoro"
    CUTIEMARK   = "Cutie Mark", "Cutie Mark"
    DANGEKI     = "Dengekimaho", "Dengekimaoh"
    NERF        = "Nerf", "Nerf"
    TRUMPKATSUMAI = "Trumpkatsumai", "Trumpkatsumai"


# Game Concepts
class TurnStructure(models.TextChoices):
    BEGIN_PHASE     = 'beginning_phase', 'Beginning Phase'
    BEGIN_UNTAP     = 'untap', 'Untap Step'
    BEGIN_UPKEEP    = 'upkeep', 'Upkeep Step'
    BEGIN_DRAW      = 'draw', 'Draw Step'
    MAIN_PHASE      = 'main_phase', 'Main Phase'
    COMBAT_PHASE    = 'combat_phase', 'Combat Phase'
    COMBAT_BEGIN    = 'beginning_combat', 'Beggining of Combat Step'
    COMBAT_ATTACK   = 'declare_attackes', 'Declare Attacker Step'
    COMBAT_BLOCK    = 'declare_blockers', 'Declare Blockers Step' 
    COMBAT_DMG      = 'assign_damage', 'Combat Damage Step'
    COMBAT_END      = 'end_combat', 'End of Combat Step'
    PC_MAIN_PHASE   = 'postcombat_main_phase', 'Post-Combat Main Phase'
    END_PHASE       = 'ending_phase', 'Ending Phase'
    END_STEP        = 'end_step', 'End step'
    END_CLEANUP     = 'cleanup', 'Cleanup step'


class Zones(models.TextChoices):
    LIBRARY     = 'library', 'Library'
    HAND        = 'hand', 'Hand'
    BATTLEFIELD = 'battlefield', 'Battelfield'
    GRAVEYARD   = 'graveyard', 'Graveyard'
    STACK       = 'stack', 'Stack'
    EXILE       = 'exile', 'Exile'
    ANTE        = 'ante', 'Ante'
    COMMAND     = 'command', 'Command Zone'
    

class MechanicType(models.TextChoices):
    KEYWORD     = 'keyword', 'Keyword'
    ACTION      = 'action', 'Action'
    ABILITYWORD = 'ability_word', 'Ability Word'
    MISC        = 'misc', 'Miscellaneous Ability'


class AbilityType(models.TextChoices):
    ACTIVATED   = 'activated', 'Activated'
    LINKED      = 'linked', 'Linked'
    LOYALTY     = 'loyalty', 'Loyalty'
    MANA        = 'mana', 'Mana'
    SPELL       = 'spell', 'Spell'
    STATIC      = 'static', 'Static'
    TRIGGER     = 'triggered', 'Triggered'
    

class EffectType(models.TextChoices):
    ONESHOT     = 'one-shot', 'One-Shot Effect'
    CONTINUOUS  = 'continuous', 'Contiuous Effect'
    TEXTCHANGE  = 'text-changing', 'Text-changing Effect'
    REPLACEMENT = 'replacement', 'Replacement Effect'
    PREVENTION  = 'prevention', 'Prevention Effect'


class LayerEffect(models.TextChoices):
    LAYER_1   = 'Layer 1', 'Layer 1: Copy effects'
    LAYER_2   = 'Layer 2', 'Layer 2: Control effects'
    LAYER_3   = 'Layer 3', 'Layer 3: Text-changing effects'
    LAYER_4   = 'Layer 4', 'Layer 4: Type-changing effects'
    LAYER_5   = 'Layer 5', 'Layer 5: Color-changing effects'
    LAYER_6   = 'Layer 6', 'Layer 6: Ability Add/Remove effects'
    LAYER_7   = 'Layer 7', 'Layer 7: Power/Toughness effects'


class DeckArchtype(models.TextChoices):
    NON         = '', ''
    AGGRO       = 'aggro', 'Aggro'
    TEMPO       = 'tempo', 'Tempo (Aggro-Control)'
    RAMP        = 'ramp', 'Ramp'
    CONTROL     = 'control', 'Control'
    STAX        = 'stax', 'Stax'
    COMBO       = 'combo', 'Combo'
    AGGROCOMBO  = 'aggro_combo', 'Aggro Combo'
    MIDRANGE    = 'midrange', 'Midrange'
    # TYPES
    ARTIFACTS   = 'artifacts', 'Artifacts'
    AURAS       = 'auras', 'Auras'
    BATTLES     = 'battles', 'Battles'
    CURSES      = 'curses', 'Curses'
    ENCHANTRESS = 'enchantress', 'Enchantress'
    EQUIPMENTS  = 'equipments', 'Equipment'
    HISTORIC    = 'historic', 'Historic'
    KINDRED     = 'kindred', 'Kindred (Tribe)'
    LANDMATTER  = 'land_matters', 'Land Matters'
    LEGENDS     = 'legends', 'Legends'
    OUTLAWS     = 'outlaws', 'Outlaws'
    PARTY       = 'party', 'Party'
    SAGAS       = 'sagas', 'Sagas'
    SHRINES     = 'shrines', 'Shrines'
    SLINGER     = 'spellslinger', 'Spellslinger'
    SNOW        = 'snow', 'Snow'
    SPACECRAFT  = 'spacecraft', 'Spacecraft'
    SUPERFRIEND = 'superfriend', 'Superfriends'
    UNNATURAL   = 'unnatural', 'Unnatural (Artifacts & Enchantments)'
    VEHICLES    = 'vehicles', 'Vehicles'
    BLOODTYPAL  = 'blood_typal', 'Blood Tokens'
    CLUETYPAL   = 'clues_typal', 'Clue Tokens'
    DUNGEON     = 'dungeons', 'Dungeons'
    FOODTYPAL   = 'food_typal', 'Food Tokens'
    LESSONS     = 'lessons', 'Lessons'
    # THEMES
    ARISTOCRATS = 'aristocrat', 'Aristocrats'
    BEATDOWN    = 'beatdown', 'Beatdown'
    BIGMANA     = 'big_mana', 'Big Mana Spells'
    BLINKER     = 'blinker', 'Blink/Flicker'
    BOUNCE      = 'bounce', 'Bounce'
    BURN        = 'burn', 'Burn'
    CANTRIP     = 'cantrip', 'Cantrips'
    CARDDRAW    = 'card_draw', 'Card Draw'
    CHAOS       = 'chaos', 'Chaos'
    CHEERIOS    = 'cheerios', 'Cheerios'
    CLONES      = 'clones', 'Clones'
    COUNTERPLUS = 'counters_plus', '+1/+1 Counters'
    COUNTERMIN  = 'counters_minus', '-1/-1 Counters'
    COUNTERKEY  = 'counters_keywords', 'Keyword Counters'
    COUNTERTYPE = 'counters_type', 'Type Counters'
    DISCARD     = 'discard', 'Discard'
    DONATE      = 'donate', 'Donate'
    ENERGY      = 'energy', 'Energy'
    EXILE       = 'exile', 'Exile'
    EXPERIENCE  = 'experience', 'Experience'
    EXTRACOMBAT = 'extra_combat', 'Extra Combats'
    EXTRAUPKEEP = 'extra_upkeeps', 'Extra Upkeep'
    FORCECOMBAT = 'forced_combat', 'Forced Combat'
    GOODSTUFF   = 'good_stuff', 'Good Stuff'
    GRAVEYARD   = 'graveyard', 'Graveyard'
    GOWIDE      = 'go_wide', 'Go-Wide'
    GROUPHUG    = 'group_hug', 'Group Hug'
    GROUPSLUG   = 'group_slug', 'Group Slug'
    IMPULSE     = 'impulse_draw', 'Impulse Draw'
    KEYWORD     = 'keyword', 'Keyword (Specific)'
    LANDFALL    = 'landfall', 'Landfall'
    LIFEDRAIN   = 'life_drain', 'Life Drain'
    LIFEGAIN    = 'life_gain', 'Life Gain'
    MANLAND     = 'man_lands', 'Land Animation'
    MILL        = 'mill', 'Mill'
    MODIFIED    = 'modified', 'Modified Creatures'
    MONARCH     = 'monarch', 'Monarch'
    MULTICOLOR  = 'multicolor', 'Multicolor Matters'
    PILLOWFORT  = 'pillow_fort', 'Pillow Fort'
    PINGER      = 'pingers', 'Pingers'
    POISON      = 'poison', 'Poison'
    POLITICS    = 'politics', 'Politics'
    POWER       = 'power_matters', 'Power Matters'
    REANIMATE   = 'reanmiator', 'Reanimator'
    SACRIFICE   = 'sacrifice', 'Sacrifice'
    SELFMILL    = 'self_mill', 'Self Mill'
    SLIGH       = 'sligh', 'Sligh'
    SNEAK       = 'Sneak', 'Sneak'
    SNEAKATTACK = 'sneak_attack', 'Sneak Attack'
    STOMPY      = 'stompy', 'Stompy'    
    TAX         = 'tax', 'Taxes'
    THEFT       = 'theft', 'Theft'
    THERING     = 'the_ring', 'The Ring'
    TOUGHNESS   = 'toughness_matters', 'Toughness Matters'
    TIMEWALKING = 'timewalking', 'Timewalking (Extra Turns)'
    TOKENS      = 'tokens', 'Tokens'
    VILLAINOUS  = 'villainous', 'Villainous Choices'
    VOLTRON     = 'voltron', 'Voltron'
    VOTING      = 'vote', 'Voting'
    WEENIES     = 'weenies', 'Weenies'
    WHEEL       = 'wheel', 'Wheel'
    XSPELLS     = 'x_spells', 'X Spells'
                

# Game Mechanics
class PartnerKeyword(models.TextChoices):
    """
    Tipos de la palabra clave 'Partner'.
    Referencia: CR 903.10
    """
    PARTNER             = 'Partner', 'Partner'
    PARTNER_WITH        = 'Partner with', 'Partner with'
    BACKGROUND          = 'Choose a Background', 'Choose a Background'
    FRIENDS_FOREVER     = 'Partner-Friends forever', 'Partner—Friends forever'
    DOCTORS_COMPANION   = "Doctor's Companion", "Doctor's Companion"
    CHARACTER_SELECT    = 'Partner-Character select', 'Partner—Character select'


# Power Level Concepts    
class PowerLevelTier(models.TextChoices):
    """
    Categorías basadas en la Honest Commander Power Scale.
    """
    PILE        = 'Pile of Cards', 'Pila de cartas (2-7)'
    CASUAL_LOW  = 'Casual Pleasant', 'Casual Agradable (8-14)'
    CASUAL_MID  = 'Casual Mid', 'Casual Intermedio (15-22)'
    CASUAL_HIGH = 'Casual High', 'Casual Fuerte (23-31)'
    OPTIMIZED   = 'Optimized', 'Optimizado / High Power (32-42)'
    CEDH        = 'cEDH', 'Commander Competitivo (43-50)'
    
    
# Collection Concepts
class CardCondition(models.TextChoices):
    NEAR_MINT   = 'NM', 'Near Mint'
    LIGHTLY     = 'LP', 'Lightly Played'
    MODERATE    = 'MP', 'Moderately Played'
    HEAVILY     = 'HP', 'Heavily Played'
    DAMAGED     = 'DMG', 'Damaged'


class CardFinish(models.TextChoices):
    NONFOIL         = 'nonfoil', 'Normal'
    FOIL            = 'foil', 'Foil'
    ETCHED          = 'etched', 'Etched Foil'
    TEXTURED        = 'textured', 'Textured Foil'
    SURGE           = 'surge', 'Surge Foil'
    NEONINK         = 'neonink', 'Neon Ink Foil'
    GILDED          = 'gilded', 'Gilded Foil'
    HALO            = 'halo', 'Halo Foil'
    CONFETTI        = 'confetti', 'Confetti Foil'
    GALAXY          = 'galaxy', 'Galaxy Foil'
    DOUBLERAINBOW   = 'doublerainbow', 'Double-Rainbow Foil'
    OILSLICK        = 'oilslick', 'Oil Slick Raised Foil'
    INVISIBLE       = 'invisible', 'Invisible Ink Foil'
    STEPCOMPLETE    = 'stepcomplete', 'Step & Complete Foil'
    AMPERSAND       = 'ampersand', 'Ampersand Foil'
    SILVERSCREEN    = 'silverscreen', 'Silver Screen Foil'
    FRACTURE        = 'fracture', 'Fracture Foil'
    RIPPLE          = 'ripple', 'Ripple Foil'
    MANA            = 'mana', 'Mana Foil'
    FIRSTPLACE      = 'firstplace', 'First Place Foil'
    PREMODERN       = 'premodern', 'Pre-Modern Foil'
    VAULT           = 'vault', 'From the Vault Foil'
    
    
# Subtypes
class ArtifactType(models.TextChoices):
    """
    Subtipos específicos para Artefactos.
    CR 205.3g
    """
    ATTRACTION      = "Attraction", "Attraction"
    BLOOD           = "Blood", "Blood"
    BOBBLEHEAD      = "Bobblehead", "Bobblehead"
    CLUE            = "Clue", "Clue"
    CONTRAPTION     = "Contraption", "Contraption"
    EQUIPMENT       = "Equipment", "Equipment"
    FOOD            = "Food", "Food"
    FORTIFICATION   = "Fortification", "Fortification"
    GOLD            = "Gold", "Gold"
    INCUBATOR       = "Incubator", "Incubator"
    INFINITY        = "Infinity", "Infinity"
    JUNK            = "Junk", "Junk"
    MAP             = "Map", "Map"
    POWERSTONE      = "Powerstone", "Powerstone"
    STONE           = "Stone", "Stone"
    TERMINUS        = "Terminus", "Terminus"
    TREASURE        = "Treasure", "Treasure"
    VEHICLE         = "Vehicle", "Vehicle"
    SPACECRAFT      = "Spacecraft", "Spacecraft"


class BattleType(models.TextChoices):
    """
    Subtipos específicos para Batallas.
    CR 205.3h
    """
    SIEGE = "Siege", "Siege"


class EnchantmentType(models.TextChoices):
    """
    Subtipos para Encantamientos. 
    CR 205.3h
    """
    AURA        = "Aura", "Aura"
    BACKGROUND  = "Background", "Background"
    CARTOUCHE   = "Cartouche", "Cartouche"
    CASE        = "Case", "Case"
    CLASS       = "Class", "Class"
    CURSE       = "Curse", "Curse"
    ROLE        = "Role", "Role"
    ROOM        = "Room", "Room"
    RUNE        = "Rune", "Rune"
    SAGA        = "Saga", "Saga"
    SHARD       = "Shard", "Shard"
    SHRINE      = "Shrine", "Shrine"


class LandType(models.TextChoices):
    """
    Subtipos para Tierras (Básicas y No Básicas). 
    CR 205.3i
    """
    # Tipos básicos
    PLAINS      = "Plains", "Plains"
    ISLAND      = "Island", "Island"
    SWAMP       = "Swamp", "Swamp"
    MOUNTAIN    = "Mountain", "Mountain"
    FOREST      = "Forest", "Forest"
    # Tipos no básicos
    CAVE        = "Cave", "Cave"
    CLOUD       = "Cloud", "Cloud"
    DESERT      = "Desert", "Desert"
    GATE        = "Gate", "Gate"
    LAIR        = "Lair", "Lair"
    LOCUS       = "Locus", "Locus"
    MINE        = "Mine", "Mine"
    SPHERE      = "Sphere", "Sphere"
    PLANET      = "Planet", "Planet"
    POWERPLANT  = "Power-Plant", "Power-Plant"
    TOWER       = "Tower", "Tower"
    TOWN        = "Town", "Town"
    URZAS       = "Urza's", "Urza's"


class BasicLandType(models.TextChoices):
    """Subtipos para Tierras Básicas."""
    PLAINS      = "Plains", "Plains"
    ISLAND      = "Island", "Island"
    SWAMP       = "Swamp", "Swamp"
    MOUNTAIN    = "Mountain", "Mountain"
    FOREST      = "Forest", "Forest"
    WASTES      = "Wastes", "Wastes"
    # Snow Lands
    SNOW_PLAINS     = "Snow-Covered Plains", "Snow-Covered Plains"
    SNOW_ISLAND     = "Snow-Covered Island", "Snow-Covered Island"
    SNOW_SWAMP      = "Snow-Covered Swamp", "Snow-Covered Swamp"
    SNOW_MOUNTAIN   = "Snow-Covered Mountain", "Snow-Covered Mountain"
    SNOW_FOREST     = "Snow-Covered Forest", "Snow-Covered Forest"
    
    
class SpellType(models.TextChoices):
    """
    Subtipos para Instants y Sorceries. 
    CR 205.3i
    """
    ADVENTURE   = "Adventure", "Adventure"
    ARCANE      = "Arcane", "Arcane"
    CHORUS      = "Chorus", "Chorus"
    LESSON      = "Lesson", "Lesson"
    OMEN        = "Omen", "Omen"
    TRAP        = "Trap", "Trap"


class PlaneswalkerType(models.TextChoices):
    """
    Subtipos de Planeswalker.
    CR ***.**
    """
    ABIAN       = "Abian", "Abian"
    AJANI       = "Ajani", "Ajani"
    AMINATOU    = "Aminatou", "Aminatou"
    ANGRATH     = "Angrath", "Angrath"
    ARLINN      = "Arlinn", "Arlinn"
    ASHIOK      = "Ashiok", "Ashiok"
    BASRI       = "Basri", "Basri"
    BOLAS       = "Bolas", "Bolas"
    CALIX       = "Calix", "Calix"
    CHANDRA     = "Chandra", "Chandra"
    DACK        = "Dack", "Dack"
    DAKKON      = "Dakkon", "Dakkon"
    DARETTI     = "Daretti", "Daretti"
    DAVRIEL     = "Davriel", "Davriel"    
    DIHADA      = "Dihada", "Dihada"
    DOMRI       = "Domri", "Domri"
    DOVIN       = "Dovin", "Dovin"    
    ELSPETH     = "Elspeth", "Elspeth"
    ERSTA       = "Ersta", "Ersta"
    ESTRID      = "Estrid", "Estrid"
    FREYALISE   = "Freyalise", "Freyalise"
    GARRUK      = "Garruk", "Garruk"
    GIDEON      = "Gideon", "Gideon"
    GRIST       = "Grist", "Grist"
    GUFF        = "Guff", "Guff"
    HUATLI      = "Huatli", "Huatli"
    JACE        = "Jace", "Jace"
    JARED       = "Jared", "Jared"
    JAYA        = "Jaya", "Jaya"
    JESKA       = "Jeska", "Jeska"
    KAITO       = "Kaito", "Kaito"
    KARN        = "Karn", "Karn"
    KASMINA     = "Kasmina", "Kasmina"
    KAYA        = "Kaya", "Kaya"
    KIORA       = "Kiora", "Kiora"
    KOTH        = "Koth", "Koth"
    LILIANA     = "Liliana", "Liliana"
    LUKKA       = "Lukka", "Lukka"
    LUXIOR      = "Luxior", "Luxior"
    NAHIRI      = "Nahiri", "Nahiri"
    NARSET      = "Narset", "Narset"
    NIKO        = "Niko", "Niko"
    NISSA       = "Nissa", "Nissa"
    NIXILIS     = "Nixilis", "Nixilis"
    OKO         = "Oko", "Oko"
    QUINTORIUS  = "Quintorius", "Quintorius"
    RAL         = "Ral", "Ral"
    ROWAN       = "Rowan", "Rowan"
    SAHEELI     = "Saheeli", "Saheeli"
    SAMUT       = "Samut", "Samut"
    SARKHAN     = "Sarkhan", "Sarkhan"
    SERRA       = "Serra", "Serra"
    SIVITRI     = "Sivitri", "Sivitri"
    SORIN       = "Sorin", "Sorin"
    SZAT        = "Szat", "Szat"
    TAMIYO      = "Tamiyo", "Tamiyo"
    TASHA       = "Tasha", "Tasha"
    TEFERI      = "Teferi", "Teferi"
    TEYO        = "Teyo", "Teferi"
    TEZZERET    = "Tezzeret", "Tezzeret"
    TIBALT      = "Tibalt", "Tibalt"
    TYVAR       = "Tyvar", "Tyvar"
    UGIN        = "Ugin", "Ugin"
    URZA        = "Urza", "Urza"
    VENSER      = "Venser", "Venser"
    VIVIEN      = "Vivien", "Vivien"
    VRASKA      = "Vraska", "Vraska"
    VRONOS      = "Vronos", "Vronos"
    WANDERER    = "Wanderer", "Wanderer"
    WILL        = "Will", "Will"
    WINDGRACE   = "Windgrace", "Windgrace"
    WRENN       = "Wrenn", "Wrenn"
    XENAGOS     = "Xenagos", "Xenagos"
    YANGGU      = "Yanggu", "Yanggu"
    YANLING     = "Yanling", "Yanling"
    # Un-games
    BOB         = "B.O.B.", "B.O.B."
    COMET       = "Comet", "Comet"
    DUCK        = "Duck", "Duck"
    DUNGEON     = "Dungeon", "Dungeon"
    # NonWalkers
    BAHAMUT         = "Bahamut", "Bahamut"
    ELLYWICK        = "Ellywick", "Ellywick"
    ELMINSTER       = "Elminster", "Elminster"
    INZERVA         = "Inzerva", "Inzerva"
    LOLTH           = "Lolth", "Lolth"
    MINSC           = "Minsc", "Minsc"
    MORDENKAINEN    = "Mordenkainen", "Mordenkainen"
    SVEGA           = "Svega", "Svega"
    ZARIEL          = "Zariel", "Zariel"
    # HotR
    DEB     = "Deb", "Deb"
    MASTER  = "Master", "Master"

