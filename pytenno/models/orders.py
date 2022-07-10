from dataclasses import dataclass
from datetime import datetime

from .enums import OrderType, Platform
from .items import _ItemInOrder
from .users import UserShort


@dataclass
class OrderCommon:
    """Common base class that orders inherit from.

    Parameters
    ----------
    id : str
        The ID of the order.

    platinum : int
        The amount of platinum per item in the order.

    quantity : int
        How many items the user is selling / buying.

    order_type : OrderType
        The type of order.

    platform : Platform
        The platform the order is on.

    region : str
        The region the order is on.

    creation_date : datetime.datetime
        The time the order was created.

    last_update : datetime.datetime
        The time the order was last updated.

    visible : bool
        Whether the order is visible to others. In this case, always True.
    """

    id: str
    platinum: int
    quantity: int
    order_type: OrderType
    platform: Platform
    region: str
    creation_date: datetime
    last_update: datetime
    visible: bool


@dataclass
class OrderRow(OrderCommon):
    """Same as OrderCommon, but with a full user model.

    Parameters
    ----------
    id : str
        The ID of the order.

    platinum : int
        The amount of platinum per item in the order.

    quantity : int
        How many items the user is selling / buying.

    order_type : OrderType
        The type of order.

    platform : Platform
        The platform the order is on.

    region : str
        The region the order is on.

    creation_date : datetime.datetime
        The time the order was created.

    last_update : datetime.datetime
        The time the order was last updated.

    visible : bool
        Whether the order is visible to others. In this case, always True.

    user : UserShort
        The user who made the order.
    """

    user: UserShort

    def from_data(node: dict):
        return OrderRow(
            user=UserShort(**node.pop("user")),
            **node,
        )

    def __repr__(self) -> str:
        return f"<OrderRow id={self.id} user={self.user.ingame_name}>"


@dataclass
class OrderFull(OrderRow):
    """Same as OrderRow, but with a full item model.

    Parameters
    ----------
    id : str
        The ID of the order.

    platinum : int
        The amount of platinum per item in the order.

    quantity : int
        How many items the user is selling / buying.

    order_type : OrderType
        The type of order.

    platform : Platform
        The platform the order is on.

    region : str
        The region the order is on.

    creation_date : datetime.datetime
        The time the order was created.

    last_update : datetime.datetime
        The time the order was last updated.

    visible : bool
        Whether the order is visible to others. In this case, always True.

    user : UserShort
        The user who made the order.

    item : ItemInOrder
        The item in the order.
    """

    item: _ItemInOrder
