import aiohttp
from types import TracebackType
from typing import Literal, Optional, Type, overload

from .constants import API_ROOT, VALID_TRANSLATIONS
from .types.droptable import DropTable
from .types.items import ItemFull, ItemShort
from .types.orders import OrderRow
from .utils import _raise_error_code, format_name


class __PyTennoBackend:
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self.session = session

    async def __aenter__(self):
        return self

    async def __aexit__(
        self,
        exctype: Optional[Type[BaseException]],
        excinst: Optional[BaseException],
        exctb: Optional[TracebackType],
    ) -> bool:
        await self.session.close()

    async def _get(self, url: str, **kwargs) -> dict[str, str | int | dict | list]:
        url = f"{API_ROOT}{url}"
        mode = getattr(self.session, kwargs.pop("method", "get"))
        response = await mode(url, **kwargs)
        if response.status != 200:
            _raise_error_code(response.status)
        return await response.json()


class __ItemBackend(__PyTennoBackend):
    async def _get_items(self, language):
        url = "/items"
        headers = {"Language": language}
        response = await self._get(url, headers=headers)

        return [ItemShort._from_data(node) for node in response["payload"]["items"]]

    async def _get_item(
        self,
        item_name,
        platform,
    ):
        url = f"/items/{format_name(item_name)}"
        headers = {"Platform": platform}
        response = await self._get(url, headers=headers)
        items = response["payload"]["item"]["items_in_set"]

        return [ItemFull._from_data(node=node) for node in items]

    async def _get_orders(
        self,
        item_name,
        include_items,
        platform,
    ):
        url = f"/items/{format_name(item_name)}/orders"
        headers = {"Platform": platform}

        if include_items:
            url += "?include=item"

        response = await self._get(url, headers=headers)
        if include_items:
            return (
                [
                    OrderRow._from_data(node=node)
                    for node in response["payload"]["orders"]
                ],
                [
                    ItemFull._from_data(node=node)
                    for node in response["include"]["item"]["items_in_set"]
                ],
            )
        return [
            OrderRow._from_data(node=node) for node in response["payload"]["orders"]
        ]

    async def _get_droptable(
        self, item_name, include_items: bool, language: VALID_TRANSLATIONS
    ):
        url = f"/items/{format_name(item_name)}/droptables"
        if include_items:
            url += "?include=item"
        headers = {"Language": language}
        response = await self._get(url, headers=headers)
        if include_items:
            return (
                DropTable._from_data(response["droptables"]),
                [
                    ItemFull._from_data(item)
                    for item in response["include"]["item"]["items_in_set"]
                ],
            )
        return DropTable._from_data(response["droptables"])


class PyTenno(__PyTennoBackend):
    def __init__(self) -> None:
        # These are hardcoded to please the linter
        # Could be easily made with __init_subclass__ but I
        # feel it's worth it for linting support
        self.session = aiohttp.ClientSession(
            headers={"content-type": "application/json"}
        )
        self.Items = Items(self)
        super().__init__()

    def __hash__(self) -> int:
        return 0


class __TennoClass:
    def __init__(self, pytenno: PyTenno):
        self.pt = pytenno


class Items(__TennoClass, __ItemBackend):
    async def get_items(self, language: VALID_TRANSLATIONS = "en") -> list[ItemShort]:
        """
        Returns all available items
        """
        return await self._get_items(language)

    @overload
    async def get_droptable(
        self,
        item_name: str,
        include_items: Literal[True],
        language: VALID_TRANSLATIONS = "en",
    ) -> tuple[list[DropTable], list[ItemFull]]:
        ...

    @overload
    async def get_droptable(
        self,
        item_name: str,
        include_items: Literal[False],
        language: VALID_TRANSLATIONS = "en",
    ) -> list[DropTable]:
        ...

    async def get_item(
        self,
        item_name: str,
        platform: Optional[Literal["pc", "xbox", "ps4", "switch"]] = "pc",
    ) -> list[ItemFull]:
        """
        Returns available information on an item.
        Items that are part of a set will have the entire set returned, as well as the blueprint and set object, if available.
        """
        return await self.pt._get_item(item_name, platform)

    @overload
    async def get_orders(
        self,
        item_name: str,
        include_items: Literal[False],
        platform: Optional[Literal["pc", "xbox", "ps4", "switch"]] = "pc",
    ) -> list[OrderRow]:
        ...

    @overload
    async def get_orders(
        self,
        item_name: str,
        include_items: Literal[True],
        platform: Optional[Literal["pc", "xbox", "ps4", "switch"]] = "pc",
    ) -> tuple[list[OrderRow], list[ItemFull]]:
        ...

    async def get_orders(
        self,
        item_name: str,
        include_items: bool,
        platform: Optional[Literal["pc", "xbox", "ps4", "switch"]] = "pc",
    ):
        return await self.pt._get_orders(item_name, include_items, platform)

    async def get_droptable(
        self,
        item_name: str,
        include_items: bool,
        language: VALID_TRANSLATIONS = "en",
    ):
        raise Exception(
            "The API on warframe.market for this feature is currently nonfunctional"
        )
        # return await self.pt._get_droptable(item_name, include_items, language)
