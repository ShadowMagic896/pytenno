from dataclasses import dataclass
from datetime import datetime
from pytenno.utils import from_data
from typing import Union

from .enums import AuctionMarking, AuctionType, Element, Platform, Polarity
from .rivens import PartialRivenAttribute
from .users import UserShort


@dataclass(kw_only=True)
class AuctionEntry:
    """Represents an auction entry.

    Attributes:
    -----------
    - `id`: :class:`str`
        The ID of the auction entry.

    - `minimum_reputation`: :class:`int`
        The minimum reputation required to bid on the auction.

    - `winner`: :class:`str` | :class:`None`
        The ID of the user who won the auction.

    - `private`: :class:`bool`
        Whether the auction is private.

    - `visible`: :class:`bool`
        Whether the auction is visible to others.

    - `note_raw`: :class:`str` | :class:`None`
        The raw note of the auction.

    - `note`: :class:`str` | :class:`None`
        The formatted note of the auction.  This is safe to include in HTML.

    - `owner`: :class:`str`
        The ID of the user who owns the auction.

    - `starting_price`: :class:`int`
        The starting price of the auction.

    - `buyout_price`: :class:`int` | :class:`None`
        The buyout price of the auction. If set to :class:`None`, the auction cannot be bought out.

    - `minimal_increment`: :class:`int`
        The minimal increment of the auction. If set to :class:`None`, the auction has no minimal increment.

    - `is_direct_sell`: :class:`bool`
        Whether the auction is a direct sell. Shortcut for ``starting_price == buyout_price``.

    - `top_bid`: :class:`int` | :class:`None`
        The top bid of the auction. If set to :class:`None`, the auction has not been bid on yet.

    - `created`: :class:`datetime`
        The time the auction was created.

    - `updated`: :class:`datetime`
        The time the auction was last updated. Bids count as updates.

    - `platform`: :class:`Platform`
        The platform the auction was created on.

    - `closed`: :class:`bool`
        Whether the auction is closed.

    - `is_marked_for`: :class:`AuctionMarking` | :class:`None`
        The action that will be executed on ``marked_operation_at``.

    - `marked_operation_at`: :class:`datetime` | :class:`None`
        The time that the auction will be deleted / archived.

    - `item`: :class:`RivenAuction` | :class:`LichAuction` | :class:`KubrowAuction`
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
    """Represents an auction entry.

    Attributes:
    -----------
    - `id`: :class:`str`
        The ID of the auction entry.

    - `minimum_reputation`: :class:`int`
        The minimum reputation required to bid on the auction.

    - `winner`: :class:`str` | :class:`None`
        The ID of the user who won the auction.

    - `private`: :class:`bool`
        Whether the auction is private.

    - `visible`: :class:`bool`
        Whether the auction is visible to others.

    - `note_raw`: :class:`str` | :class:`None`
        The raw note of the auction.

    - `note`: :class:`str` | :class:`None`
        The formatted note of the auction.  This is safe to include in HTML.

    - `owner`: :class:`UserShort`
        The owner of the auction.

    - `starting_price`: :class:`int`
        The starting price of the auction.

    - `buyout_price`: :class:`int` | :class:`None`
        The buyout price of the auction. If set to :class:`None`, the auction cannot be bought out.

    - `minimal_increment`: :class:`int`
        The minimal increment of the auction. If set to :class:`None`, the auction has no minimal increment.

    - `is_direct_sell`: :class:`bool`
        Whether the auction is a direct sell. Shortcut for ``starting_price == buyout_price``.

    - `top_bid`: :class:`int` | :class:`None`
        The top bid of the auction. If set to :class:`None`, the auction has not been bid on yet.

    - `created`: :class:`datetime`
        The time the auction was created.

    - `updated`: :class:`datetime`
        The time the auction was last updated. Bids count as updates.

    - `platform`: :class:`Platform`
        The platform the auction was created on.

    - `closed`: :class:`bool`
        Whether the auction is closed.

    - `is_marked_for`: :class:`AuctionMarking` | :class:`None`
        The action that will be executed on ``marked_operation_at``.

    - `marked_operation_at`: :class:`datetime` | :class:`None`
        The time that the auction will be deleted / archived.

    - `item`: :class:`RivenAuction` | :class:`LichAuction` | :class:`KubrowAuction`
        The item being bid upon.
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

    Attributes:
    -----------
    - `type`: :class:`AuctionType`
        The type of the auction. In this case, ``lich``.

    - `weapon_url`: :class:`str`
        The URL of the weapon.

    - `element`: :class:`Element`
        The element of the weapon.

    - `damage`: :class:`int`
        The damage of the weapon.

    - `having_ephemera`: :class:`bool`
        Whether the weapon has an ephemera.

    - `quirk`: :class:`str` | :class:`None`
        The quirk of the lich.

    - `name`: :class:`str` | :class:`None`
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

    Attributes:
    -----------
    - `type`: :class:`AuctionType`
        The type of the auction. In this case, ``kubrow``.

    - `name`: :class:`str`
        The name of the kubrow.
    """

    type: AuctionType  # kubrow
    name: str


@dataclass
class RivenAuction:
    """Represents a riven auction.

    Attributes:
    -----------
    - `type`: :class:`AuctionType`
        The type of the auction. In this case, ``riven``.

    - `attributes`: :class:list[:class:`PartialRivenAttribute`]
        The attributes of the riven.

    - `name`: :class:`str`
        The name of the riven.

    - `mastery_level`: :class:`int`
        The mastery level of the riven.

    - `re_rolls`: :class:`int`
        The number of times the riven has been rerolled.

    - `weapon_url_name`: :class:`str`
        The URL of the weapon the riven is for.

    - `polarity`: :class:`Polarity`
        The polarity of the riven.

    - `mod_rank`: :class:`int`
        The rank of the riven.
    """

    type: AuctionType # riven
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
