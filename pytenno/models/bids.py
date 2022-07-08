from dataclasses import dataclass
from datetime import datetime


@dataclass
class Bid:
    """Represents a bid on an auction.

    Attributes:
    -----------
    - `id`: :class:`int`
        The ID of the bid.

    - `auction`: :class:`str`
        The ID of the auction the bid is on.

    - `user`: :class:`str`
        The ID of the user who made the bid.

    - `value`: :class:`int`
        The amount of platinum placed on the bid.

    - `created`: :class:`datetime`
        The time the bid was made.

    - `updated`: :class:`datetime`
        The time the bid was last updated.
    """

    id: str
    auction: str
    user: str
    value: int
    created: datetime
    updated: datetime
