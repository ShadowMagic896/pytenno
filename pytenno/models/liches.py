from dataclasses import dataclass

from .enums import AnimationFormat, Element, IconFormat


@dataclass
class LichWeapon:
    id: str
    url_name: str
    icon: str
    icon_format: IconFormat
    thumb: str
    item_name: str


@dataclass
class LichEphemera:
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
    id: str
    url_name: str
    item_name: str
    description: str
    group: str  # Does not belong to any specific enum
