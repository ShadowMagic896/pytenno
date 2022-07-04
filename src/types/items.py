from dataclasses import dataclass

from ..constants import ASSET_ROOT
from ..utils import _create_languages
from .enums import ItemRarity, Subtype
from .formats import ObjectID


@dataclass
class LangInItem:
    item_name: str
    description: str
    wiki_link: str | None

    # {name: str, description: str}
    # Already translated
    drop: list["Drop"]


@dataclass
class Drop:

    # translated name of the location / item
    name: str

    # link to the internal or extarnal source with information about that location
    link: str


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
    mod_max_rank: int | None

    subtypes: list[Subtype] | None
    tags: list[str]

    # will be introduced in update 1.8.3 and will replace rank for sculptures
    cyan_stars: int | None
    amber_stars: int | None

    ducats: int

    def __repr__(self):
        return f"<ItemCommon id={self.id} url_name={self.url_name} tags={self.tags}>"


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

    def __repr__(self):
        return f"<ItemInOrder id={self.id} url_name={self.url_name} tags={self.tags}>"


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

    def __repr__(self):
        return f"<ItemFull id={self.id} url_name={self.url_name} tags={self.tags} rarity={self.rarity}>"

    def _from_data(node: dict):
        return ItemFull(
            id=node["id"],
            url_name=ObjectID(node["url_name"]),
            icon=f"{ASSET_ROOT}/{node['icon']}",
            thumb=f"{ASSET_ROOT}/{node['thumb']}",
            sub_icon=f"{ASSET_ROOT}/{node['sub_icon']}"
            if node["sub_icon"] is not None
            else None,
            mod_max_rank=node.get("mod_max_rank", None),
            subtypes=[Subtype[name] for name in node.pop("subtypes", [])],
            tags=node["tags"],
            cyan_stars=node.get("cyan_stars", None),
            amber_stars=node.get("amber_stars", None),
            ducats=node["ducats"],
            set_root=node["set_root"],
            mastery_rank=node["mastery_level"],
            rarity=ItemRarity[rarity]
            if (rarity := node.get("rarity", None)) is not None
            else None,
            trading_tax=node["trading_tax"],
            **_create_languages(node, LangInItem, Drop),
        )


@dataclass
class ItemShort:
    id: ObjectID
    url_name: str
    thumb: str
    item_name: str

    def _from_data(node: dict):
        return ItemShort(
            id=node["id"],
            url_name=node["url_name"],
            thumb=node["thumb"],
            item_name=node["item_name"],
        )

    def __repr__(self):
        return f"<ItemShort id={self.id} url_name={self.url_name}>"
