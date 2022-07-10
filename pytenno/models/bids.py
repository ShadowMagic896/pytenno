from dataclasses import dataclass
from datetime import datetime


@dataclass
class Bid:
    """Represents a bid on an auction.

    Parameters
    ----------
    id : int
        The ID of the bid.

    auction : str
        The ID of the auction the bid is on.

    user : str
        The ID of the user who made the bid.

    value : int
        The amount of platinum placed on the bid.

    created : datetime.datetime
        The time the bid was made.

    updated : datetime.datetime
        The time the bid was last updated.
    """

    id: str
    auction: str
    user: str
    value: int
    created: datetime
    updated: datetime
