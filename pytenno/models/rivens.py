from dataclasses import dataclass

from .enums import (
    IconFormat,
    MeasurementUnit,
    RivenAttributeGroup,
    RivenType,
    RivenWeaponGroup,
    RivenWeaponType,
)


@dataclass
class RivenItem:
    """Represents a riven item.

    Attributes:
    -----------
    - `id`: :class:`str`
        The ID of the riven item.

    - `item_name`: :class:`str`
        The name of the riven item.

    - `item_url_name`: :class:`str`
        The URL name of the riven item.

    - `group`: :class:`RivenWeaponGroup`
        The group of the riven item.

    - `riven_type`: :class:`RivenType`
        The type of the riven item.

    - `icon`: :class:`str`
        The icon URL of the riven item.

    - `icon_format`: :class:`IconFormat`
        The format of the icon URL of the riven item.

    - `thumb`: :class:`str`
        The thumbnail URL of the riven item.
    """

    id: str
    item_name: str
    url_name: str
    group: RivenWeaponGroup
    riven_type: RivenType
    icon: str
    icon_format: IconFormat
    thumb: str


@dataclass
class RivenAttribute:
    """Represents a riven attribute. Most rivens have multiple attributes.

    Attributes:
    -----------
    - `id`: :class:`str`
        The ID of the riven attribute.

    - `url_name`: :class:`str`
        The URL name of the riven attribute.

    - `group`: :class:`RivenAttributeGroup`
        The group of the riven attribute

    - `prefix`: :class:`str`
        The prefix of the riven attribute.
        Example: "hexi"

    - `suffix`: :class:`str`
        The suffix of the riven attribute.
        Example: "bin"

    - `positive_is_negative`: :class:`bool`
        Whether the positive attribute is actually negative.
        Example: Recoil, Reload Speed, etc.

    - `exclusive_to`: :class:`list[:class:`RivenWeaponType`]]` | :class:`None`
        The types of weapons that the attribute is exclusive to. :class:`None` if it is not exclusive to any weapon.

    - `effect`: :class:`str`
        The effect of the riven attribute. Depends on the requested language.

    - `units`: :class:`MeasurementUnit`
        What the riven attribute is measured in.

    - `negative_only`: :class:`bool`
        Whether the attribute only appears as a negative.

    - `search_only`: :class:`bool`
        Whether the attribute only appears in search results.
    """

    id: str
    url_name: str
    group: RivenAttributeGroup
    prefix: str
    suffix: str
    positive_is_negative: bool
    exclusive_to: list[RivenWeaponType] | None
    effect: str
    units: MeasurementUnit
    negative_only: bool
    search_only: bool


@dataclass
class PartialRivenAttribute:
    """Represents a partial riven attribute.

    Attributes:
    -----------
    - `positive`: :class:`bool`
        Whether the attribute is positive.

    - `value`: :class:`int`
        The value of the attribute.

    - `url_name`: :class:`str`
        The URL name of the attribute.
    """

    positive: bool
    value: int
    url_name: str
