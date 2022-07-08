from dataclasses import dataclass

from .enums import Faction


@dataclass
class Location:
    """Represents a location.

    Attributes:
    -----------
    - `id`: :class:`str`
        The ID of the location.

    - `icon`: :class:`str`
        The icon URL of the location.

    - `thumb`: :class:`str`
        The thumbnail URL of the location.

    - `faction`: :class:`Faction`
        The faction of the location.

    - `name`: :class:`str`
        The name of the location.

    - `node_name`: :class:`str`
        The name of the node the location is on.
    """

    id: str
    icon: str
    thumb: str
    faction: Faction
    name: str
    node_name: str
