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
    id: str

    # 	Name of the weapon, depends on the requested language
    item_name: str
    url_name: str

    # Group of the item, like shotgin, rifle, melee, etc.
    # Used for grouping within UI elements.
    group: RivenWeaponGroup

    # Type of the riven mod, to restrict certain attributes to specific types
    riven_type: RivenType

    # path to the icon asset file
    icon: str
    icon_format: IconFormat
    thumb: str


@dataclass
class RivenAttribute:
    id: str
    url_name: str

    # Group of the attribute, like top, melee, etc.
    # Used for grouping within UI elements.
    group: RivenAttributeGroup
    prefix: str
    suffix: str

    # Negative value of this attribute indicate that attribute is positive, e.g. Recoil
    positive_is_negative: bool

    # This attribute is only available on specific types of items, check item property: riven_type.
    # If null, then this attribute can be selected on every item.
    exclusive_to: list[RivenWeaponType] | None

    # Name of the attribute, depends on the requested language
    effect: str

    # Measurement units
    units: MeasurementUnit

    # This attribute occurs only as a negative.
    negative_only: bool

    # Used only while searching for auctions
    search_only: bool


@dataclass
class PartialRivenAttribute:
    positive: bool
    value: int
    url_name: str
