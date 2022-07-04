from dataclasses import dataclass

from .enums import OrderType, Platform
from .formats import DateTime, ObjectID
from .items import ItemInOrder
from .users import UserShort


@dataclass
class OrderCommon:
    id: ObjectID
    platinum: int
    quantity: int
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

    def _from_data(node: dict):
        return OrderRow(
            id=ObjectID(node["id"]),
            platinum=node["platinum"],
            quantity=node["quantity"],
            order_type=OrderType[node["order_type"]],
            platform=Platform[node["platform"]],
            region=node["region"],
            creation_date=DateTime(node["creation_date"]),
            last_update=DateTime(node["last_update"]),
            visible=node["visible"],
            user=UserShort._from_data(node["user"]),
        )

    def __repr__(self) -> str:
        return f"<OrderRow id={self.id} user={self.user.ingame_name}>"


@dataclass
class OrderFull(OrderCommon):
    item: ItemInOrder
