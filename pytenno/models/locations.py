from dataclasses import dataclass
from .enums import Faction

@dataclass
class Location:
    id: str
    icon: str
    thumb: str
    faction: Faction
    name: str
    node_name: str