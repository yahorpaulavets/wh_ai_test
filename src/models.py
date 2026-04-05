from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from enum import Enum
import uuid


class PieceType(str, Enum):
    CHARACTER = "character"
    VEHICLE = "vehicle"
    MONSTER = "monster"
    INFANTRY = "infantry"


class PieceFaction(str, Enum):
    CHAOS = "chaos"
    SPACE_MARINES = "space_marines"
    IMPERIUM = "imperium"
    ORKS = "orks"
    TYRANIDS = "tyranids"
    NECRONS = "necrons"
    ELDAR = "eldar"


class RangeWeapon(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    name: str
    R: int
    AN: int
    BS: int
    S: int
    AP: int
    D: str
    keywords: List[str] = []


class MeleeWeapon(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    name: str
    AN: int
    WS: int
    S: int
    AP: int
    D: str
    keywords: List[str] = []


class GamePiece(BaseModel):
    model_config = ConfigDict(use_enum_values=True, arbitrary_types_allowed=True)

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    row: int
    col: int
    name: str
    faction: PieceFaction
    type: PieceType
    M: int
    T: int
    SV: int
    ISV: Optional[int] = None
    W: int
    W_max: int
    LD: int
    OC: int
    RangeWeapon: List[RangeWeapon] = []
    MeleeWeapon: List[MeleeWeapon] = []
    symbol: str = "♟"
    keywords: List[str] = []
    base_size: int = 1  # Размер базы в клетках (1 = 1x1, 3 = 3x3, 5 = 5x5)


# ✅ Модели запросов
class MoveRequest(BaseModel):
    piece_id: str
    new_row: int
    new_col: int


class AttackRequestWH(BaseModel):
    attacker_id: str
    defender_id: str
    weapon_type: str = "melee"
    weapon_index: int = 0