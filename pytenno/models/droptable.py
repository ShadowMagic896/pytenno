from dataclasses import dataclass

from .missions import DroptableMission, DroptableNPC, DroptableRelic


@dataclass
class DropTable:
    """Represents an item's drop table.

    Attributes:
    -----------
    - `missions`: :class:`list`[:class:`Mission`]
        The missions where the item can be found.

    - `relics`: :class:`list`[:class:`RelicDrop`]
        The relic in which parts for the item can be found.

    - `npc`: :class:`list`[:class:`NPC`]
        The NPCs where the item can be found.
    """

    missions: list[DroptableMission]
    relics: list[DroptableRelic]
    npc: list[DroptableNPC]

    def from_data(node: dict):
        return DropTable(
            [DroptableMission.from_data(mission) for mission in node["missions"]],
            [DroptableRelic.from_data(relic) for relic in node["relics"]],
            [DroptableNPC.from_data(npc) for npc in node["npc"]],
        )


@dataclass
class Drop:
    """Represents an item's drop.

    Attributes:
    -----------
    - `name`: :class:`str`
        The translated name of the location / item.

    - `link`: :class:`str`
        Link to the internal or extarnal source with information about that location.
    """
    
    name: str
    link: str
