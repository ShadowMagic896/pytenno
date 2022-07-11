from dataclasses import dataclass

from .missions import DroptableMission, DroptableNPC, DroptableRelic


@dataclass
class DropTable:
    """Represents an item's drop table."""

    missions: list[DroptableMission]
    """The missions where the item can be found."""
    relics: list[DroptableRelic]
    """The relic in which parts for the item can be found."""
    npc: list[DroptableNPC]
    """The NPCs where the item can be found."""

    def from_data(node: dict):
        return DropTable(
            [DroptableMission.from_data(mission) for mission in node["missions"]],
            [DroptableRelic.from_data(relic) for relic in node["relics"]],
            [DroptableNPC.from_data(npc) for npc in node["npc"]],
        )


@dataclass
class Drop:
    """Represents an item's drop."""

    name: str
    """The translated name of the location / item."""
    link: str
    """Link to the internal or extarnal source with information about that location."""
