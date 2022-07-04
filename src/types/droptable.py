from dataclasses import dataclass

from .missions import NPC, Mission, RelicDrop


@dataclass
class DropTable:
    missions: list[Mission]
    relics: list[RelicDrop]
    npc: list[NPC]

    def _from_data(node: dict):
        return DropTable(
            [Mission._from_data(mission) for mission in node["missions"]],
            [RelicDrop._from_data(relic) for relic in node["relics"]],
            [NPC._from_data(npc) for npc in node["npc"]],
        )


@dataclass
class Drop:

    # translated name of the location / item
    name: str

    # link to the internal or extarnal source with information about that location
    link: str
