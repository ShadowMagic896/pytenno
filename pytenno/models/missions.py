from dataclasses import dataclass

from .enums import ItemRarity, RelicQuality, Rotation, Stage, Subtype


@dataclass
class DroptableMission:
    """Represents a mission.

    Attributes:
    -----------
    - `mission_id`: :class:`str`
        The ID of the mission.

    - `node_id`: :class:`str`
        The ID of the node the mission is on.

    - `rarity`: :class:`ItemRarity`
        The rarity of the item found in the mission.

    - `rate`: :class:`int` | :class:`float`
        The rate of the item found in the mission.

    - `item_subtype`: :class:`Subtype`
        The subtype of the item found in the mission.

    - `rotation`: :class:`Rotation`
        The rotation where the item can be found.

    - `stage`: :class:`Stage`
        The stage of the item found in the mission

    - `relics`: :class:[:class:`RelicDrop`]
        Relics that can be found in the mission.

    - `npc`: :class:list[:class:`NPC`]
        The NPCs where the item can be found.
    """

    mission_id: str
    node_id: str
    rarity: ItemRarity
    rate: int | float
    item_subtype: Subtype
    rotation: Rotation
    stage: Stage
    relics: list["DroptableRelic"]
    npc: list["DroptableNPC"]


@dataclass
class PartialMission:
    """Represents a partial mission.

    Attributes:
    -----------
    - `id`: :class:`str`
        The ID of the mission.

    - `icon`: :class:`str`
        The icon URL of the mission.

    - `thumb`: :class:`str`
        The thumbnail URL of the mission.

    - `name`: :class:`str`
        The name of the mission.
    """

    id: str
    icon: str
    thumb: str
    name: str


@dataclass
class DroptableRelic:
    """Represents a relic drop in a mission

    Attributes:
    -----------
    - `id`: :class:`str`
        The ID of the relic.

    - `rarity`: :class:`ItemRarity`
        The rarity of the item found in the relic.

    - `rate`: :class:dict[:class:RelicQuality, :class:int | :class:float]
        A mapping of relic quality to the rate of the relic dropping.
    """

    id: str
    rarity: ItemRarity
    rate: dict[RelicQuality, int | float]


@dataclass
class DroptableNPC:
    """Represents a NPC in a mission

    Attributes:
    -----------
    - `id`: :class:`str`
        The ID of the NPC.

    - `icon`: :class:`str`
        The icon URL of the NPC.

    - `thumb`: :class:`str`
        The thumbnail URL of the NPC.

    - `name`: :class:`str`
        The name of the NPC.
    """

    id: str
    icon: str
    thumb: str
    name: str
