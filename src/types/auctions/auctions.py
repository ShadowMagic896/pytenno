from dataclasses import dataclass
from typing import Union

from ..enums import AuctionMarking, Platform
from ..formats import DateTime, ObjectID
from ..users import UserShort
from .kubrows import KubrowAuction
from .liches import LichAuction
from .rivens import RivenAuction


@dataclass
class AuctionEntry:
    id: ObjectID

    # Minimal amount of reputation that is required to participate in this auction
    minimal_reputation: int

    # If winner is set, auction is in the paused state. While on pause, bids can't be added, but can be removed.
    winner: str | None

    private: bool
    visible: bool

    # Raw format string, use it inside textarea, for editing purposes.
    note_raw: str

    # It's safe to inject this into html, this is refined, formatted string from MD processor.
    note: str

    owner: ObjectID
    starting_price: int

    # if buyout_price is set to null, that means inf.
    buyout_price: int

    minimal_increment: int | None

    # Shortcut to starting_price == buyout_price, means that auction is not an auction, but an order
    is_direct_sell: bool

    top_bid: int | None
    created: DateTime

    # Last time auction was updated, eighter by owner or by placing a bid.
    updated: DateTime

    platform: Platform

    # Auction is closed, and was marked for removal or archiving, no one can add or remove bids now.
    closed: bool

    # Auction will be removed or archivated after marked_operation_at
    is_marked_for: AuctionMarking | None

    marked_operation_for: DateTime | None

    item: Union[RivenAuction, LichAuction, KubrowAuction]


@dataclass
class AuctionEntryExpanded(AuctionEntry):
    # owner will contain userShort model

    # override AuctionEntry's value, otherwise it will be just an ID
    owner: UserShort
