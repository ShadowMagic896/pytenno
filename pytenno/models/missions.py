from dataclasses import dataclass

from .enums import ItemRarity, RelicQuality, Rotation, Stage, Subtype


@dataclass
class DroptableMission:
    """Represents a mission.

    Parameters
    ----------
    mission_id : str
        The ID of the mission.

    node_id : str
        The ID of the node the mission is on.

    rarity : ItemRarity
        The rarity of the item found in the mission.

    rate : int | float
        The rate of the item found in the mission.

    item_subtype : Subtype
        The subtype of the item found in the mission.

    rotation : Rotation
        The rotation where the item can be found.

    stage : Stage
        The stage of the item found in the mission

    relics : list[RelicDrop]
        Relics that can be found in the mission.

    npc : list[NPC]
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

    Parameters
    ----------
    id : str
        The ID of the mission.

    icon : str
        The icon URL of the mission.

    thumb : str
        The thumbnail URL of the mission.

    name : str
        The name of the mission.
    """

    id: str
    icon: str
    thumb: str
    name: str


@dataclass
class DroptableRelic:
    """Represents a relic drop in a mission

    Parameters
    ----------
    id : str
        The ID of the relic.

    rarity : ItemRarity
        The rarity of the item found in the relic.

    rate dict[RelicQuality, int | float]
        A mapping of relic quality to the rate of the relic dropping.
    """

    id: str
    rarity: ItemRarity
    rate: dict[RelicQuality, int | float]


@dataclass
class DroptableNPC:
    """Represents a NPC in a mission

    Parameters
    ----------
    id : str
        The ID of the NPC.

    icon : str
        The icon URL of the NPC.

    thumb : str
        The thumbnail URL of the NPC.

    name : str
        The name of the NPC.
    """

    id: str
    icon: str
    thumb: str
    name: str
