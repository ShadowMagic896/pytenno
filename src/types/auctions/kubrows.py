from dataclasses import dataclass

from ..enums import AuctionType


@dataclass
class KubrowAuction:
    type: AuctionType  # kubrow
    name: str
