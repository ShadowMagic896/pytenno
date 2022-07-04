from dataclasses import dataclass

from ..enums import AnimationFormat, AuctionType, Element, IconFormat
from ..formats import ObjectID


@dataclass
class LichWeapon:
    id: ObjectID
    url_name: str
    icon: str
    icon_format: IconFormat
    thumb: str
    item_name: str


@dataclass
class LichEphemera:
    id: ObjectID
    url_name: str
    icon: str
    icon_format: IconFormat
    thumb: str
    animation: str
    animation_format: AnimationFormat
    element: Element
    item_name: str


@dataclass
class LickQuirk:
    id: ObjectID
    url_name: str
    item_name: str
    description: str
    group: str  # Does not belong to any specific enum


@dataclass
class LichAuction:
    type: AuctionType  # lich
    weapon_url_name: str
    element: Element
    damage: int
    ephemera: bool
    quirk: str
    name: str  # Unused by API
