from dataclasses import dataclass
from typing import Union

from .enums import FishSize, ItemRarity, RelicQuality
from .formats import ObjectID


@dataclass
class LangInItem:
    item_name: str
    description: str
    wiki_link: str | None

    # {name: str, description: str}
    # Already translated
    drop: list[dict[str, str]]


@dataclass
class ItemCommon:
    # [a-z] snake case name of the item
    id: ObjectID
    url_name: str

    icon: str
    thumb: str

    # Usually, if item is part of set and not set itself, it will have sub_icon like
    # Mirage Blueprint is part of Mirage Set, therefore the icon will be the Mirage warframe icon, and the sub_icon will be the blueprint icon
    sub_icon: str

    # In next API verison:
    # max_rank: int
    mod_max_rank: int

    subtypes: Union[RelicQuality, FishSize] | None
    tags: list[str]

    # will be introduced in update 1.8.3 and will replace rank for sculptures
    cyan_stars: int
    amber_stars: int

    ducats: int


@dataclass
class ItemInOrder(ItemCommon):
    """Same as ItemCommon but with item name translations"""

    en: dict[str, str]
    ru: dict[str, str]
    ko: dict[str, str]
    fr: dict[str, str]
    de: dict[str, str]
    sv: dict[str, str]
    zh_hant: dict[str, str]
    zh_hans: dict[str, str]
    pt: dict[str, str]
    es: dict[str, str]
    pl: dict[str, str]


@dataclass
class ItemFull(ItemInOrder):
    """same as ItemInOrder, but lang related fields contain more infos, + rarity, set_root, MR, trading tax."""

    set_root: bool
    mastery_rank: int
    rarity: ItemRarity
    trading_tax: int

    en: LangInItem
    ru: LangInItem
    ko: LangInItem
    fr: LangInItem
    de: LangInItem
    sv: LangInItem
    zh_hant: LangInItem
    zh_hans: LangInItem
    pt: LangInItem
    es: LangInItem
    pl: LangInItem


@dataclass
class ItemShort:
    id: ObjectID
    url_name: str
    thumb: str
    item_name: str
