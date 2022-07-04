from dataclasses import dataclass

from .enums import (
    FishSize,
    FortunaFishQuality,
    ItemRarity,
    RelicQuality,
    Rotation,
    Stage,
)
from .formats import ObjectID


@dataclass
class Mission:
    mission_id: ObjectID
    node_id: ObjectID
    rarity: ItemRarity
    rate: int | float
    item_subtype: RelicQuality | FishSize | FortunaFishQuality
    rotation: Rotation
    stage: Stage
    relics: list["RelicDrop"]
    npc: list["NPC"]


@dataclass
class PartialMission:
    id: ObjectID
    icon: str
    thumb: str
    name: str


@dataclass
class RelicDrop:
    id: ObjectID
    rarity: ItemRarity
    rate: dict[RelicQuality, int | float]


@dataclass
class NPC:
    id: ObjectID
    icon: str
    thumb: str
    name: str
