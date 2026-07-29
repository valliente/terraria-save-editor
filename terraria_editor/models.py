from dataclasses import dataclass, field
from typing import List, Tuple

@dataclass
class Color:
    r: int = 255
    g: int = 255
    b: int = 255

    def to_hex(self) -> str:
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    @classmethod
    def from_hex(cls, hex_str: str) -> 'Color':
        hex_str = hex_str.lstrip('#')
        if len(hex_str) == 6:
            r = int(hex_str[0:2], 16)
            g = int(hex_str[2:4], 16)
            b = int(hex_str[4:6], 16)
            return cls(r, g, b)
        return cls(255, 255, 255)

@dataclass
class InventoryItem:
    id: int = 0
    stack: int = 0
    prefix: int = 0
    favorite: bool = False

    @property
    def name(self) -> str:
        return ITEM_NAMES.get(self.id, f"Unknown Item ({self.id})") if self.id > 0 else "Empty"

    @property
    def prefix_name(self) -> str:
        return PREFIX_NAMES.get(self.prefix, f"Prefix {self.prefix}") if self.prefix > 0 else "None"

GAME_MODES = {
    0: "Classic",
    1: "Mediumcore",
    2: "Hardcore",
    3: "Journey"
}

GAME_MODE_IDS = {v: k for k, v in GAME_MODES.items()}

@dataclass
class Player:
    version: int = 230
    file_type: str = "relogic"
    name: str = "Terrarian"
    difficulty: int = 0  # 0: Classic, 1: Mediumcore, 2: Hardcore, 3: Journey
    play_time_ticks: int = 0
    hair_style: int = 0
    hair_dye: int = 0
    hide_visuals: int = 0
    hide_visuals2: int = 0
    hide_misc: int = 0
    skin_variant: int = 0
    hp: int = 100
    max_hp: int = 100
    mana: int = 20
    max_mana: int = 20
    extra_accessory: bool = False
    downed_dd2_event: bool = False
    tax_collector_paid: bool = False
    
    # Colors
    hair_color: Color = field(default_factory=lambda: Color(215, 90, 55))
    skin_color: Color = field(default_factory=lambda: Color(255, 125, 90))
    eye_color: Color = field(default_factory=lambda: Color(105, 80, 55))
    shirt_color: Color = field(default_factory=lambda: Color(175, 165, 140))
    undershirt_color: Color = field(default_factory=lambda: Color(160, 180, 215))
    pants_color: Color = field(default_factory=lambda: Color(255, 230, 175))
    shoe_color: Color = field(default_factory=lambda: Color(160, 105, 60))

    # Inventory slots (50 main + 8 coins/ammo + 20 armor/accessories + 5 dye + 5 misc + banks)
    inventory: List[InventoryItem] = field(default_factory=list)
    armor: List[InventoryItem] = field(default_factory=list)
    dye: List[InventoryItem] = field(default_factory=list)
    misc_eq: List[InventoryItem] = field(default_factory=list)

    def __post_init__(self):
        if not self.inventory:
            self.inventory = [InventoryItem() for _ in range(58)] # 50 inv + 4 coins + 4 ammo
        if not self.armor:
            self.armor = [InventoryItem() for _ in range(20)] # armor + accessories + vanity
        if not self.dye:
            self.dye = [InventoryItem() for _ in range(10)]
        if not self.misc_eq:
            self.misc_eq = [InventoryItem() for _ in range(5)]

# Curated Item Database for Quick Add & Name Lookup
ITEM_NAMES = {
    0: "Empty",
    1: "Iron Broadsword",
    2: "Dirt Block",
    3: "Stone Block",
    4: "Iron Axe",
    5: "Wood",
    6: "Iron Hammer",
    7: "Iron Bow",
    8: "Torch",
    29: "Life Crystal",
    109: "Mana Crystal",
    71: "Copper Coin",
    72: "Silver Coin",
    73: "Gold Coin",
    74: "Platinum Coin",
    3507: "Solar Flare Helmet",
    3508: "Solar Flare Breastplate",
    3509: "Solar Flare Leggings",
    4956: "Zenith",
    4923: "Terraprisma",
    3542: "Meowmere",
    3540: "Star Wrath",
    3460: "Luminite Bar",
    3456: "Solar Fragment",
    3457: "Vortex Fragment",
    3458: "Nebula Fragment",
    3459: "Stardust Fragment",
    50: "Magic Mirror",
    3199: "Cell Phone",
    5358: "Shellphone",
    1326: "Rod of Discord",
    5010: "Rod of Harmony",
    497: "Minishark",
    1553: "Megashark",
    3476: "S.D.M.G.",
    2997: "Ankh Shield",
    3110: "Terraspark Boots",
    1163: "Tome of Infinite Wisdom",
    # 1.4.5 Dead Cells Crossover
    6001: "The Flint",
    6002: "Mushroom Staff",
    6003: "Beheaded Vanity Head",
    6004: "Beheaded Vanity Body",
    6005: "Beheaded Vanity Legs",
    # 1.4.5 Palworld Collab
    6010: "Digtoise Pickaxe",
    6011: "Pal Sphere",
    # 1.4.5 New Whips
    6020: "Moon Lord Whip",
    6021: "Stardust Whip",
    6022: "Plantera Whip",
    6023: "Slime Whip",
    # 1.4.5 Transformation Mounts
    6030: "Velociraptor Mount",
    6031: "Bat Mount",
    6032: "Rat Mount",
    6033: "Fairy Mount",
    6034: "Roller Skates",
}

PREFIX_NAMES = {
    0: "None",
    1: "Large",
    2: "Massive",
    3: "Dangerous",
    4: "Savage",
    5: "Sharp",
    6: "Pointy",
    7: "Tiny",
    8: "Terrible",
    9: "Small",
    10: "Dull",
    11: "Unhappy",
    12: "Bulky",
    13: "Shameful",
    14: "Heavy",
    15: "Light",
    16: "Sighted",
    17: "Rapid",
    18: "Hasty",
    19: "Intimidating",
    20: "Deadly",
    21: "Staunch",
    22: "Awful",
    23: "Lethargic",
    24: "Awkward",
    25: "Powerful",
    26: "Mystic",
    27: "Adept",
    28: "Masterful",
    29: "Inept",
    30: "Ignorant",
    31: "Deranged",
    32: "Intense",
    33: "Taboo",
    34: "Celestial",
    35: "Furious",
    36: "Keen",
    37: "Superior",
    38: "Forceful",
    39: "Broken",
    40: "Damaged",
    41: "Shoddy",
    42: "Quick",
    43: "Deadly",
    44: "Agile",
    45: "Nimble",
    46: "Murderous",
    47: "Slow",
    48: "Sluggish",
    49: "Lazy",
    50: "Annoying",
    51: "Nasty",
    52: "Manic",
    53: "Hurtful",
    54: "Strong",
    55: "Unpleasant",
    56: "Weak",
    57: "Ruthless",
    58: "Frenzying",
    59: "Godly",
    60: "Demonic",
    61: "Zealous",
    62: "Hard",
    63: "Guarding",
    64: "Armored",
    65: "Warding",
    66: "Arcane",
    67: "Precise",
    68: "Lucky",
    69: "Jagged",
    70: "Spiked",
    71: "Angry",
    72: "Menacing",
    73: "Brisk",
    74: "Fleeting",
    75: "Hasty",
    76: "Quick",
    77: "Wild",
    78: "Rash",
    79: "Intrepid",
    80: "Violent",
    81: "Legendary",
    82: "Unreal",
    83: "Mythical",
}
