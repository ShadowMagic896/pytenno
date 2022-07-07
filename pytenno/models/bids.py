from dataclasses import dataclass
from datetime import datetime


@dataclass
class Bid:
    id: str
    auction: str
    user: str
    value: int
    created: datetime
    updated: datetime
