from dataclasses import dataclass
from datetime import datetime

from pytenno.utils import from_data

from .enums import OrderType, Platform
from .items import ItemInOrder
from .users import UserShort


@dataclass
class OrderCommon:
    """Common base class that orders inherit from."""

    id: str
    """The ID of the order."""
    platinum: int
    """The amount of platinum per item in the order."""
    quantity: int
    """How many items the user is selling / buying."""
    order_type: OrderType
    """The type of order."""
    platform: Platform
    """The platform the order is on."""
    region: str
    """The region the order is on."""
    creation_date: datetime
    """The time the order was created."""
    last_update: datetime
    """The time the order was last updated."""
    visible: bool
    """Whether the order is visible to others. In this case, always True."""


@dataclass
class OrderCreated(OrderCommon):
    """Represents an Order after it has been passed to the API
    and is now created."""

    item: ItemInOrder
    """The item in the order."""

    def from_data(data: dict):
        return OrderCreated(
            item=from_data(ItemInOrder, data.pop("item")),
        )


@dataclass
class OrderRow(OrderCommon):
    """Same as OrderCommon, but with a full user model."""

    user: UserShort
    """The user who made the order."""

    def from_data(node: dict):
        return OrderRow(
            user=UserShort(**node.pop("user")),
            **node,
        )

    def __repr__(self) -> str:
        return f"<OrderRow id={self.id} user={self.user.ingame_name}>"


@dataclass
class OrderFull(OrderRow):
    """Same as OrderRow, but with a full item model."""

    item: ItemInOrder
    """The item in the order."""
