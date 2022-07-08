from dataclasses import dataclass
from datetime import datetime
from pytenno.utils import from_data
from typing import Union

from .enums import AuctionMarking, AuctionType, Element, Platform, Polarity
from .rivens import PartialRivenAttribute
from .users import UserShort


@dataclass(kw_only=True)
class AuctionEntry:
    id: str

    # Minimal amount of reputation that is required to participate in this auction
    minimal_reputation: int

    # If winner is set, auction is in the paused state. While on pause, bids can't be added, but can be removed.
    winner: str | None = None

    private: bool
    visible: bool

    # Raw format string, use it inside textarea, for editing purposes.
    note_raw: str

    # It's safe to inject this into html, this is refined, formatted string from MD processor.
    note: str

    owner: str
    starting_price: int

    # if buyout_price is set to null, that means inf.
    buyout_price: int | None = None

    minimal_increment: int | None = None

    # Shortcut to starting_price == buyout_price, means that auction is not an auction, but an order
    is_direct_sell: bool

    top_bid: int | None = None
    created: datetime

    # Last time auction was updated, eighter by owner or by placing a bid.
    updated: datetime

    platform: Platform

    # Auction is closed, and was marked for removal or archiving, no one can add or remove bids now.
    closed: bool

    # Auction will be removed or archived after marked_operation_at
    is_marked_for: AuctionMarking | None = None

    marked_operation_for: datetime | None = None

    item: Union["RivenAuction", "LichAuction", "KubrowAuction"]


@dataclass
class AuctionEntryExpanded(AuctionEntry):
    # owner will contain userShort model

    # override AuctionEntry's value, otherwise it will be just an ID
    owner: UserShort

    def _from_data(node: dict):
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
    type: AuctionType  # lich
    weapon_url_name: str
    element: Element
    damage: int
    having_ephemera: bool
    quirk: str = None
    name: str = None  # Unused by API


@dataclass
class KubrowAuction:
    type: AuctionType  # kubrow
    name: str


@dataclass
class RivenAuction:
    # type of the item, in this case it's riven
    type: AuctionType

    # 1 - 4 items
    attributes: list[PartialRivenAttribute]

    name: str
    mastery_level: int
    re_rolls: int
    weapon_url_name: str
    polarity: Polarity

    # 0 - 10
    mod_rank: int

    def _from_data(node: dict):
        return RivenAuction(
            attributes=[
                from_data(PartialRivenAttribute, x) for x in node.pop("attributes")
            ],
            **node,
        )
