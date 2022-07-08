from dataclasses import dataclass

from .enums import AnimationFormat, Element, IconFormat


@dataclass
class LichWeapon:
    """Represents a lich weapon.

    Attributes:
    -----------
    - `id`: :class:`str`
        The ID of the weapon.

    - `url_name`: :class:`str`
        The URL name of the weapon.

    - `icon`: :class:`str`
        The icon URL of the weapon.

    - `icon_format`: :class:`IconFormat`
        The format of the weapon's icon.

    - `icon_format`: :class:`IconFormat`
        The format of the weapon's icon.

    - `thumb`: :class:`str`
        The thumbnail URL of the weapon.

    - `item_name`: :class:`str`
        The name of the weapon.
    """

    id: str
    url_name: str
    icon: str
    icon_format: IconFormat
    thumb: str
    item_name: str


@dataclass
class LichEphemera:
    """Represents a lich ephemera.

    Attributes:
    -----------
    - `id`: :class:`str`
        The ID of the ephemera.

    - `url_name`: :class:`str`
        The URL name of the ephemera.

    - `icon`: :class:`str`
        The icon URL of the ephemera.

    - `icon_format`: :class:`IconFormat`
        The format of the ephemera's icon.

    - `thumb`: :class:`str`
        The thumbnail URL of the ephemera.

    - `animation`: :class:`str`
        The animation URL of the ephemera.

    - `animation_format`: :class:`AnimationFormat`
        The format of the ephemera's animation.

    - `element`: :class:`Element`
        The element of the ephemera.

    - `item_name`: :class:`str`
        The name of the ephemera.
    """

    id: str
    url_name: str
    icon: str
    icon_format: IconFormat
    thumb: str
    animation: str
    animation_format: AnimationFormat
    element: Element
    item_name: str


@dataclass
class LichQuirk:
    """Represents a lich quirk.

    Attributes:
    -----------
    - `id`: :class:`str`
        The ID of the quirk.

    - `url_name`: :class:`str`
        The URL name of the quirk.

    - `item_name`: :class:`str`
        The name of the quirk.

    - `description`: :class:`str`
        The description of the quirk.

    - `group`: :class:`str`
        The group of the quirk. Does not belong to any specific enum
    """

    id: str
    url_name: str
    item_name: str
    description: str
    group: str
