from dataclasses import dataclass

from ..formats import DateTime, ObjectID


@dataclass
class Bid:
    id: ObjectID
    auction: ObjectID
    user: ObjectID
    value: int
    created: DateTime
    updated: DateTime
