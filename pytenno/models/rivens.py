from dataclasses import dataclass

from .enums import (
    IconFormat,
    MeasurementUnit,
    RivenAttributeGroup,
    RivenWeaponGroup,
    RivenWeaponType,
)


@dataclass
class RivenItem:
    """Represents a riven item.

    Parameters
    -----------
    id : str
        The ID of the riven item.

    item_name : str
        The name of the riven item.

    item_url_name : str
        The URL name of the riven item.

    group : RivenWeaponGroup
        The group of the riven item.

    riven_type : RivenType
        The type of the riven item.

    icon : str
        The icon URL of the riven item.

    icon_format : IconFormat
        The format of the icon URL of the riven item.

    thumb : str
        The thumbnail URL of the riven item.
    """

    id: str
    item_name: str
    url_name: str
    group: RivenWeaponGroup
    riven_type: RivenWeaponType
    icon: str
    icon_format: IconFormat
    thumb: str


@dataclass
class RivenAttribute:
    """Represents a riven attribute. Most rivens have multiple attributes.

    Parameters
    -----------

    id : str
        The ID of the riven attribute.

    url_name : str
        The URL name of the riven attribute.

    group : RivenAttributeGroup
        The group of the riven attribute

    prefix : str
        The prefix of the riven attribute.
        Example: "hexi"

    suffix : str
        The suffix of the riven attribute.
        Example: "bin"

    positive_is_negative : bool
        Whether the positive attribute is actually negative.
        Example: Recoil, Reload Speed, etc.

    exclusive_to : list[RivenWeaponType] , optional
        The types of weapons that the attribute is exclusive to. None if it is not exclusive to any weapon.

    effect : str
        The effect of the riven attribute. Depends on the requested language.

    units : MeasurementUnit
        What the riven attribute is measured in.

    negative_only : bool
        Whether the attribute only appears as a negative.

    search_only : bool
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

    Parameters
    -----------
    positive : bool
        Whether the attribute is positive.

    value : int
        The value of the attribute.

    url_name : str
        The URL name of the attribute.
    """

    positive: bool
    value: int
    url_name: str
