from dataclasses import dataclass

from .enums import OrderType, Platform
from .formats import DateTime, ObjectID
from .items import ItemInOrder
from .users import UserShort


@dataclass
class OrderCommon:
    id: ObjectID
    platinum: int
    qualtity: int
    order_type: OrderType
    platform: Platform
    region: str
    creation_date: DateTime
    last_update: DateTime

    # always true for this model, exists only for backward compatibility
    visible: bool


@dataclass
class OrderRow(OrderCommon):
    user: UserShort


@dataclass
class OrderFull(OrderCommon):
    item: ItemInOrder
