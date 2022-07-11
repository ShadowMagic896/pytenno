from dataclasses import dataclass
from pytenno.constants import VALID_TRANSLATIONS_RAW

from pytenno.utils import from_data

from .droptable import Drop
from .enums import IconFormat, ItemRarity, Subtype


@dataclass
class LangInItem:
    """Represents an item's localized name.

    Parameters
    ----------
    item_name : str
        The translated name of the item.

    description : str
        The translated description of the item.

    wiki_link : str , optional
        The link to the wiki page of the item.

    drop : list[Drop]
        Where the item can be found.
    """

    item_name: str
    description: str
    wiki_link: str | None
    drop: list[Drop]


@dataclass(kw_only=True)
class ItemCommon:
    """Common base class that an item can inherit from.

    Parameters
    ----------
    id : str
        The ID of the item.

    url_name : str
        The URL name of the item.

    icon : str
        The URL of the item's icon.

    icon_format : IconFormat
        The format of the item's icon.

    sub_icon : str , optional
        The URL of the item's sub icon. For example if the item is part of a set, `icon` will the icon of the set, while `sub_icon` will be the icon of the item in the set.

    thumb : str
        The URL of the item's thumbnail.

    tags : list[str]
        The tags of the item.

    mod_max_rank : int
        The maximum rank of the item.
        SOON TO BE: max_rank

    subtypes : list[Subtype] , optional
        The subtypes of the item.

    cyan_stars : int
        The number of cyan stars the item has.

    amber_stars : int
        The number of amber stars the item has.

    ducats : int
        The ducat worth of the item.
    """

    id: str
    url_name: str
    icon: str
    icon_format: IconFormat | None = None
    sub_icon: str = None
    thumb: str
    tags: list[str]
    mod_max_rank: int | None = None
    subtypes: list[Subtype] | None = None
    cyan_stars: int | None = None
    amber_stars: int | None = None
    ducats: int | None = None

    def __repr__(self):
        return f"<ItemCommon id={self.id} url_name={self.url_name} tags={self.tags}>"


@dataclass(kw_only=True)
class TranslatedItemName:
    item_name: str

@dataclass(kw_only=True)
class ItemInOrder(ItemCommon):
    en: TranslatedItemName
    ru: TranslatedItemName
    ko: TranslatedItemName
    fr: TranslatedItemName
    de: TranslatedItemName
    sv: TranslatedItemName
    zh_hant: TranslatedItemName
    zh_hans: TranslatedItemName
    pt: TranslatedItemName
    es: TranslatedItemName
    pl: TranslatedItemName

    def from_data(node: dict):
        [node.__setitem__(lang, TranslatedItemName(item_name=node[lang]["item_name"])) for lang in VALID_TRANSLATIONS_RAW]
        # Sets all of the languages to their TransLatedItemName objects.
        # A bit odd to call __setitem__ manually, but it lets it work in a listcomp so meh.
        return from_data(ItemInOrder, node)

    def __repr__(self):
        return f"<ItemInOrder id={self.id} url_name={self.url_name} tags={self.tags}>"



@dataclass(kw_only=True)
class ItemFull(ItemInOrder):
    """same as ItemInOrder, but lang related fields contain more infos, + rarity, set_root, MR, trading tax.


    Parameters
    ----------
    id : str
        The ID of the item.

    url_name : str
        The URL name of the item.

    icon : str
        The URL of the item's icon.

    icon_format : IconFormat
        The format of the item's icon.

    sub_icon : str , optional
        The URL of the item's sub icon. For example if the item is part of a set, `icon` will the icon of the set, while `sub_icon` will be the icon of the item in the set.

    thumb : str
        The URL of the item's thumbnail.

    tags : list[str]
        The tags of the item.

    mod_max_rank : int
        The maximum rank of the item.
        SOON TO BE: max_rank

    subtypes : list[Subtype] , optional
        The subtypes of the item.

    cyan_stars : int
        The number of cyan stars the item has.

    amber_stars : int
        The number of amber stars the item has.

    ducats : int
        The ducat worth of the item.

    set_root : bool
        Whether the item is part of a set.

    mastery_level : int
        The mastery level of the item.

    rarity : ItemRarity , optional
        The rarity of the item. If None, the item does not have any specific rarity.

    trading_tax : int
        The trading tax of the item.

    quantity_for_set : int , optional
        The quantity of the item required to obtain the set.

    en : LangInItem
        The english language of the item.

    ru : LangInItem
        The russian language of the item.

    ko : LangInItem
        The korean language of the item.

    fr : LangInItem
        The french language of the item.

    de : LangInItem
        The german language of the item.

    sv : LangInItem
        The swedish language of the item.

    zh_hant : LangInItem
        The chinese traditional language of the item.

    zh_hans : LangInItem
        The chinese simplified language of the item.

    pt : LangInItem
        The portuguese language of the item.

    es : LangInItem
        The spanish language of the item.

    pl : LangInItem
        The polish language of the item.
    """

    set_root: bool
    mastery_level: int
    rarity: ItemRarity | None = None
    trading_tax: int
    quantity_for_set: int = None

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
    """Represents a simplified version of an item.

    Parameters
    ----------
    id : str
        The ID of the item.

    url_name : str
        The URL name of the item.

    thumb : str
        The URL of the item's thumbnail.

    item_name : str
        The name of the item.
    """

    id: str
    url_name: str
    thumb: str
    item_name: str

    def __repr__(self):
        return f"<ItemShort id={self.id} url_name={self.url_name}>"
