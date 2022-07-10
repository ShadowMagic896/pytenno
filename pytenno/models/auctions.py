from dataclasses import dataclass
from datetime import datetime
from typing import Union

from ..utils import from_data
from .enums import AuctionMarking, AuctionType, Element, Platform, Polarity
from .rivens import PartialRivenAttribute
from .users import UserShort


@dataclass(kw_only=True)
class AuctionEntry:
    """Represents an auction entry.

    Parameters
    ----------
    id : str
        The ID of the auction entry.

    minimum_reputation : int
        The minimum reputation required to bid on the auction.

    winner : str , optional
        The ID of the user who won the auction.

    private : bool
        Whether the auction is private.

    visible : bool
        Whether the auction is visible to others.

    note_raw : str , optional
        The raw note of the auction.

    note : str , optional
        The formatted note of the auction.  This is safe to include in HTML.

    owner : str
        The ID of the user who owns the auction.

    starting_price : int
        The starting price of the auction.

    buyout_price : int , optional
        The buyout price of the auction. If set to None, the auction cannot be bought out.

    minimal_increment : int
        The minimal increment of the auction. If set to None, the auction has no minimal increment.

    is_direct_sell : bool
        Whether the auction is a direct sell. Shortcut for ``starting_price == buyout_price``.

    top_bid : int , optional
        The top bid of the auction. If set to None, the auction has not been bid on yet.

    created : datetime.datetime
        The time the auction was created.

    updated : datetime.datetime
        The time the auction was last updated. Bids count as updates.

    platform : Platform
        The platform the auction was created on.

    closed : bool
        Whether the auction is closed.

    is_marked_for : AuctionMarking , optional
        The action that will be executed on ``marked_operation_at``.

    marked_operation_at : datetime.datetime , optional
        The time that the auction will be deleted / archived.

    item : RivenAuction | LichAuction | KubrowAuction
        The item being bid upon.
    """

    id: str
    minimal_reputation: int
    winner: str | None = None
    private: bool
    visible: bool
    note_raw: str
    note: str
    owner: str
    starting_price: int
    buyout_price: int | None = None
    minimal_increment: int | None = None
    is_direct_sell: bool
    top_bid: int | None = None
    created: datetime
    updated: datetime
    platform: Platform
    closed: bool
    is_marked_for: AuctionMarking | None = None
    marked_operation_for: datetime | None = None
    item: Union["RivenAuction", "LichAuction", "KubrowAuction"]


@dataclass
class AuctionEntryExpanded(AuctionEntry):
    """Same as `AuctionEntry`, but with a full user model for ``.owner``

    Parameters
    ----------
    id : str
        The ID of the auction entry.

    minimum_reputation : int
        The minimum reputation required to bid on the auction.

    winner : str , optional
        The ID of the user who won the auction.

    private : bool
        Whether the auction is private.

    visible : bool
        Whether the auction is visible to others.

    note_raw : str , optional
        The raw note of the auction.

    note : str , optional
        The formatted note of the auction.  This is safe to include in HTML.

    owner : str
        The ID of the user who owns the auction.

    starting_price : int
        The starting price of the auction.

    buyout_price : int , optional
        The buyout price of the auction. If set to None, the auction cannot be bought out.

    minimal_increment : int
        The minimal increment of the auction. If set to None, the auction has no minimal increment.

    is_direct_sell : bool
        Whether the auction is a direct sell. Shortcut for ``starting_price == buyout_price``.

    top_bid : int , optional
        The top bid of the auction. If set to None, the auction has not been bid on yet.

    created : datetime.datetime
        The time the auction was created.

    updated : datetime.datetime
        The time the auction was last updated. Bids count as updates.

    platform : Platform
        The platform the auction was created on.

    closed : bool
        Whether the auction is closed.

    is_marked_for : AuctionMarking , optional
        The action that will be executed on ``marked_operation_at``.

    marked_operation_at : datetime.datetime , optional
        The time that the auction will be deleted / archived.

    item : RivenAuction | LichAuction | KubrowAuction
        The item being bid upon.

    owner : UserShort
        The owner of the auction.
    """

    owner: UserShort

    def from_data(node: dict):
        # deepcode ignore
        return AuctionEntryExpanded(
            # file deepcode ignore WrongNumberOfArguments
            owner=from_data(UserShort, node.pop("owner")),
            item=from_data(RivenAuction, item)
            if (t := (item := node.pop("item"))["type"]) == "riven"
            else from_data(LichAuction, item)
            if t == "lich"
            else from_data(KubrowAuction, item),
            **node,
        )


@dataclass(kw_only=True)
class LichAuction:
    """Represents a lich auction.

    Parameters
    ----------
    type : AuctionType
        The type of the auction. In this case, ``lich``.

    weapon_url : str
        The URL of the weapon.

    element : Element
        The element of the weapon.

    damage : int
        The damage of the weapon.

    having_ephemera : bool
        Whether the weapon has an ephemera.

    quirk : str , optional
        The quirk of the lich.

    name : str , optional
        The name of the lich. Unused by the API.
    """

    type: AuctionType  # lich
    weapon_url_name: str
    element: Element
    damage: int
    having_ephemera: bool
    quirk: str | None = None
    name: str | None = None  # Unused by API


@dataclass
class KubrowAuction:
    """Represents a kubrow auction.

    Parameters
    ----------
    type : AuctionType
        The type of the auction. In this case, ``kubrow``.

    name : str
        The name of the kubrow.
    """

    type: AuctionType  # kubrow
    name: str


@dataclass
class RivenAuction:
    """Represents a riven auction.

    Parameters
    ----------
    type : AuctionType
        The type of the auction. In this case, ``riven``.

    attributes : list[PartialRivenAttribute]
        The attributes of the riven.

    name : str
        The name of the riven.

    mastery_level : int
        The mastery level of the riven.

    re_rolls : int
        The number of times the riven has been rerolled.

    weapon_url_name : str
        The URL of the weapon the riven is for.

    polarity : Polarity
        The polarity of the riven.

    mod_rank : int
        The rank of the riven.
    """

    type: AuctionType  # riven
    attributes: list[PartialRivenAttribute]
    name: str
    mastery_level: int
    re_rolls: int
    weapon_url_name: str
    polarity: Polarity
    mod_rank: int

    def from_data(node: dict):
        return RivenAuction(
            attributes=[
                from_data(PartialRivenAttribute, x) for x in node.pop("attributes")
            ],
            **node,
        )
