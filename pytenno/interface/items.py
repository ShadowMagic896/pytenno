from typing import Literal, Optional, overload

from .._backends.items import ItemsBackend
from ..constants import VALID_LANGUAGES
from ..models.droptable import DropTable
from ..models.enums import Platform
from ..models.items import ItemFull, ItemShort
from ..models.orders import OrderRow


class Items(ItemsBackend):
    """Class for the items backend."""
    async def get_items(self, language: Optional[VALID_LANGUAGES] = None) -> list[ItemShort]:
        """Gets all items.

        Parameters
        ----------
        language : Optional[VALID_LANGUAGES]
            The language of the items. Default: ``None``, meaning the default set during client construction.

        Returns
        -------
        list[ItemShort]

        Example
        -------
        >>> async with PyTenno() as pytenno:
        >>>     items = await pytenno.items.get_items()
        >>>     for item in items:
        >>>         print(item.url_name)
        """
        return await self._get_items(language)

    async def get_item(
        self,
        item_name: str,
        *,
        platform: Optional[Platform] = Platform.pc,
    ) -> list[ItemFull]:
        """Gets the item with the given name, as well as related items (such as items of the same set).

        Parameters
        ----------
        item_name : str
            The name of the item.
        platform : Platform
            The platform of the item. Default: Platform.pc.

        Returns
        -------
        list[ItemFull]

        Example
        -------
        >>> async with PyTenno() as pytenno:
        >>>     items = await pytenno.items.get_item("kuva_bramma")
        >>>     for item in items:
        >>>         print(item.url_name)
        """
        return await self._get_item(item_name, platform)

    @overload
    async def get_orders(
        self,
        item_name: str,
        include_items: Literal[False],
        platform: Optional[Platform] = Platform.pc,
    ) -> list[OrderRow]:
        ...

    @overload
    async def get_orders(
        self,
        item_name: str,
        include_items: Literal[True],
        platform: Optional[Platform] = Platform.pc,
    ) -> tuple[list[OrderRow], list[ItemFull]]:
        ...

    async def get_orders(
        self,
        item_name: str,
        include_items: bool,
        platform: Optional[Platform] = Platform.pc,
    ):
        """Gets the orders of the given item.

        Parameters
        ----------
        item_name : str
            The name of the item.
        include_items : bool
            Whether to include information about the item requested.
        platform : Platform
            The platform of the item. Default: Platform.pc.

        Returns
        -------
        list[OrderRow] | tuple(list[OrderRow], list[ItemFull])

        Example
        -------
        >>> async with PyTenno() as pytenno:
        >>>     orders, items = await pytenno.items.get_orders("kuva_bramma", include_items=True)
        >>>     for order in orders:
        >>>         print(order.user.ingame_name)
        >>>     for item in items:
        >>>         print(item.url_name)
        """
        return await self._get_orders(item_name, include_items, platform)

    @overload
    async def get_droptable(
        self,
        item_name: str,
        include_items: Literal[False],
        language: Optional[VALID_LANGUAGES] = None,
    ) -> DropTable:
        ...

    @overload
    async def get_droptable(
        self,
        item_name: str,
        include_items: Literal[True],
        language: Optional[VALID_LANGUAGES] = None,
    ) -> tuple[DropTable, list[ItemFull]]:
        ...

    async def get_droptable(
        self,
        item_name: str,
        include_items: bool,
        language: Optional[VALID_LANGUAGES] = None,
    ):
        """Gets the droptable of the given item.

        Parameters
        ----------
        item_name : str
            The name of the item.
        include_items : bool
            Whether to include information about the item requested.
        language : Optional[VALID_LANGUAGES]
            The language of the droptable. Default: ``None``, meaning the default set during client construction.

        Returns
        -------
        DropTable | tuple(DropTable, list[ItemFull])

        Example
        -------
        >>> async with PyTenno() as pytenno:
        >>>     droptable, items = await pytenno.items.get_droptable("kuva_bramma", include_items=True)
        >>>     print(droptable.relics, droptable.missions)
        >>>     for item in items:
        >>>         print(item.url_name)

        """
        raise Exception(
            "The API on warframe.market for this feature is currently nonfunctional"
        )
