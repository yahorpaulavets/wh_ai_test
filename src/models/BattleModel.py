import json
from enum import Enum
from typing import Optional


class BattleModel:
    def __init__(self):
        self.M = 0
        self.T = 0
        self.SV = 0
        self.ISV = 0
        self.W = 0
        self.LD = 0
        self.OC = 0

        self.INDEX = ""

        self.name = ""
        self.range_weapon: Optional[list:RangeWeapon] = None
        self.melee_weapon: Optional[list:MeleeWeapon] = None
        self.abilities: Optional[Abilities] = None

    def to_dict(self):
        return {
            "Name": self.name,
            "M": self.M,
            "T": self.T,
            "SV": self.SV,
            "ISV": self.ISV,
            "W": self.W,
            "LD": self.LD,
            "OC": self.OC,
            "RangeWeapon": [rw.to_dict() for rw in self.range_weapon],
            "MeleeWeapon": [mw.to_dict() for mw in self.melee_weapon],
        }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False, default=str)


class RangeWeapon:

    def __init__(self):
        self.R = 0
        self.AN = 0
        self.BS = 0
        self.S = 0
        self.AP = 0
        self.D = 0

        self.name = ""
        self.keywords = []

    def to_dict(self):
        return {
            "Name": self.name,
            "R": self.R,
            "AN": self.AN,
            "BS": self.BS,
            "S": self.S,
            "AP": self.AP,
            "D": self.D,
            "keywords": [s.value for s in self.keywords]
        }


class MeleeWeapon:

    def __init__(self):
        self.AN = 0
        self.WS = 0
        self.S = 0
        self.AP = 0
        self.D = 0

        self.name = ""
        self.keywords = []

    def to_dict(self):
        return {
            "Name": self.name,
            "AN": self.AN,
            "WS": self.WS,
            "S": self.S,
            "AP": self.AP,
            "D": self.D,
            "keywords": [s.value for s in self.keywords]
        }


class Abilities:

    def __init__(self):
        self.faction = []
        self.core = []
        self.personal = []


class WeaponKeywords(Enum):
    POISON_D3 = "отравленное D3"
    TWIN = "спаренное"
    DISSECTING = "рассекающее"
    POISON = "отравленное"
    IGNORE_COVER = "игнорирует укрытия"
    TORENT = "потоковое"
    LETHAL_HITS = "летальные попадания"
    PSYCHIC = "психическое"
    PRECISE = "точное"


class CoreAbilities(Enum):
    FIGHT_FIRST = "Сражаться первым"


class Factions(Enum):
    DAEMONS_OF_SLAANESH = "Демоны Сланеш"


class PersonalAbilities(Enum):
    PRINCE_OF_SEDUCTION = "Аура принца соблазна: все вражеские модели в радиусе 15 дюймов вычитают 3 из хит рола по этой модели"
    VAMPIRE = "Каждое устранение вражеское модели восполняет D6 ранее потерянных ран"
    SEDUCTION_OF_ENEMY = "При искушении вражеское БЕ в 16-и дюймах, БЕ не может применять способности и получает D3 смертельных ранений"
