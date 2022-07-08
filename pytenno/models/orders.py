from dataclasses import dataclass
from datetime import datetime

from .enums import OrderType, Platform
from .items import ItemInOrder
from .users import UserShort


@dataclass
class OrderCommon:
    """Common base class that orders inherit from.

    Attributes:
    -----------
    - `id`: :class:`str`
        The ID of the order.

    - `platinum`: :class:`int`
        The amount of platinum per item in the order.

    - `quantity`: :class:`int`
        How many items the user is selling / buying.

    - `order_type`: :class:`OrderType`
        The type of order.

    - `platform`: :class:`Platform`
        The platform the order is on.

    - `region`: :class:`str`
        The region the order is on.

    - `creation_date`: :class:`datetime`
        The time the order was created.

    - `last_update`: :class:`datetime`
        The time the order was last updated.

    - `visible`: :class:`bool`
        Whether the order is visible to others. In this case, always :class:`True`.
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
    """Same as :class:`OrderCommon`, but with a full user model.

    Attributes:
    -----------
    - `id`: :class:`str`
        The ID of the order.

    - `platinum`: :class:`int`
        The amount of platinum per item in the order.

    - `quantity`: :class:`int`
        How many items the user is selling / buying.

    - `order_type`: :class:`OrderType`
        The type of order.

    - `platform`: :class:`Platform`
        The platform the order is on.

    - `region`: :class:`str`
        The region the order is on.

    - `creation_date`: :class:`datetime`
        The time the order was created.

    - `last_update`: :class:`datetime`
        The time the order was last updated.

    - `visible`: :class:`bool`
        Whether the order is visible to others. In this case, always :class:`True`.

    - `user`: :class:`UserShort`
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
    """Same as :class:`OrderRow`, but with a full item model.

    Attributes:
    -----------
    - `id`: :class:`str`
        The ID of the order.

    - `platinum`: :class:`int`
        The amount of platinum per item in the order.

    - `quantity`: :class:`int`
        How many items the user is selling / buying.

    - `order_type`: :class:`OrderType`
        The type of order.

    - `platform`: :class:`Platform`
        The platform the order is on.

    - `region`: :class:`str`
        The region the order is on.

    - `creation_date`: :class:`datetime`
        The time the order was created.

    - `last_update`: :class:`datetime`
        The time the order was last updated.

    - `visible`: :class:`bool`
        Whether the order is visible to others. In this case, always :class:`True`.

    - `user`: :class:`UserShort`
        The user who made the order.

    - `item`: :class:`ItemInOrder`
        The item in the order.
    """

    item: ItemInOrder
