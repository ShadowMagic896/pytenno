from dataclasses import dataclass
from datetime import datetime

from .enums import OrderType, Platform
from .items import ItemInOrder
from .users import UserShort


@dataclass
class OrderCommon:
    id: str
    platinum: int
    quantity: int
    order_type: OrderType
    platform: Platform
    region: str
    creation_date: datetime
    last_update: datetime

    # always true for this model, exists only for backward compatibility
    visible: bool


@dataclass
class OrderRow(OrderCommon):
    user: UserShort

    def _from_data(node: dict):
        return OrderRow(
            user=UserShort(**node.pop("user")),
            **node,
        )

    def __repr__(self) -> str:
        return f"<OrderRow id={self.id} user={self.user.ingame_name}>"


@dataclass
class OrderFull(OrderCommon):
    item: ItemInOrder
