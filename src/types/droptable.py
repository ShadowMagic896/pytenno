from dataclasses import dataclass

from .missions import NPC, Mission, RelicDrop


@dataclass
class DropTable:
    missions: list[Mission]
    relics: list[RelicDrop]
    npc: list[NPC]
