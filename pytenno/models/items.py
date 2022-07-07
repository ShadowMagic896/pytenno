from dataclasses import dataclass, field

from .enums import ItemRarity, Subtype


@dataclass
class Drop:

    # translated name of the location / item
    name: str

    # link to the internal or extarnal source with information about that location
    link: str


@dataclass
class LangInItem:
    item_name: str
    description: str
    wiki_link: str | None

    # {name: str, description: str}
    # Already translated
    drop: list[Drop]


@dataclass(kw_only=True)
class ItemCommon:
    # [a-z] snake case name of the item
    id: str
    url_name: str

    icon: str
    icon_format: str
    sub_icon: str = None
    thumb: str

    tags: list[str]

    # In next API verison:
    # max_rank: int
    mod_max_rank: int | None = None

    subtypes: list[Subtype] | None = None

    # will be introduced in update 1.8.3 and will replace rank for sculptures
    cyan_stars: int | None = None
    amber_stars: int | None = None

    ducats: int | None = None

    def __repr__(self):
        return f"<ItemCommon id={self.id} url_name={self.url_name} tags={self.tags}>"


@dataclass(kw_only=True)
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


@dataclass(kw_only=True)
class ItemFull(ItemInOrder):
    """same as ItemInOrder, but lang related fields contain more infos, + rarity, set_root, MR, trading tax."""

    set_root: bool
    mastery_level: int
    rarity: ItemRarity
    trading_tax: int
    quantity_for_set: int = field(default=1)

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


@dataclass
class ItemShort:
    id: str
    url_name: str
    thumb: str
    item_name: str

    def __repr__(self):
        return f"<ItemShort id={self.id} url_name={self.url_name}>"
