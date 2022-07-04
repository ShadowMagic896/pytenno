from dataclasses import dataclass

from ..enums import (
    AuctionType,
    IconFormat,
    Polarity,
    RivenAttributeGroup,
    RivenGroup,
    RivenType,
)
from ..formats import ObjectID


@dataclass
class RivenItem:
    id: ObjectID

    # 	Name of the weapon, depends on the requested language
    item_name: str
    url_name: str

    # Group of the item, like shotgin, rifle, melee, etc.
    # Used for grouping within UI elements.
    group: RivenGroup

    # Type of the riven mod, to restrict certain attributes to specific types
    riven_type: RivenType

    # path to the icon asset file
    icon: str
    icon_format: IconFormat
    thumb: str


@dataclass
class RivenAttribute:
    id: ObjectID
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
    exclusive_to: RivenGroup | None

    # Name of the attribute, depends on the requested language
    effect: str

    # Measurement units
    units: str | None

    # This attribute occurs only as a negative.
    negative_only: bool

    # Used only while searching for auctions
    search_only: bool


@dataclass
class RivenAuction:
    # type of the item, in this case it's riven
    type: AuctionType

    # 1 - 4 items
    attributes: list["PartialRivenAttribute"]

    name: str
    mastery_level: int
    re_rolls: int
    weapon_url_name: str
    polarity: Polarity

    # 0 - 10
    mod_rank: int


@dataclass
class PartialRivenAttribute:
    positive: str
    value: int
    url_name: str
