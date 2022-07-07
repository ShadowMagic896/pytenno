from dataclasses import dataclass

from .enums import (
    FishSize,
    FortunaFishQuality,
    ItemRarity,
    RelicQuality,
    Rotation,
    Stage,
    Subtype,
)


@dataclass
class Mission:
    mission_id: str
    node_id: str
    rarity: ItemRarity
    rate: int | float
    item_subtype: Subtype
    rotation: Rotation
    stage: Stage
    relics: list["RelicDrop"]
    npc: list["NPC"]


@dataclass
class PartialMission:
    id: str
    icon: str
    thumb: str
    name: str


@dataclass
class RelicDrop:
    id: str
    rarity: ItemRarity
    rate: dict[RelicQuality, int | float]


@dataclass
class NPC:
    id: str
    icon: str
    thumb: str
    name: str
