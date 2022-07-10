from ..constants import VALID_LANGUAGES
from ..models.droptable import DropTable
from ..models.items import ItemFull, ItemShort
from ..models.orders import OrderFull, OrderRow
from ..utils import format_name, from_data
from .core import BackendAdapter


class ItemsBackend(BackendAdapter):
    async def _get_items(self, language: str):
        url = "/items"
        headers = {"Language": language}
        response = await self._backend._request(url, headers=headers)

        return [from_data(ItemShort, node) for node in response["payload"]["items"]]

    async def _get_item(
        self,
        item_name: str,
        platform: str,
    ):
        url = f"/items/{format_name(item_name)}"
        headers = {"Platform": str(platform)}
        response = await self._backend._request(url, headers=headers)
        if response is None:
            return None
        items = response["payload"]["item"]["items_in_set"]

        return [from_data(ItemFull, node) for node in items]

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

        response = await self._backend._request(url, headers=headers)
        if include_items:
            return (
                [from_data(OrderRow, node) for node in response["payload"]["orders"]],
                [
                    from_data(ItemFull, node)
                    for node in response["include"]["item"]["items_in_set"]
                ],
            )
        return [from_data(OrderRow, node) for node in response["payload"]["orders"]]

    async def _get_droptable(
        self, item_name, include_items: bool, language: VALID_LANGUAGES
    ):
        url = f"/items/{format_name(item_name)}/droptables"
        if include_items:
            url += "?include=item"
        headers = {"Language": language}
        response = await self._backend._request(url, headers=headers)
        if include_items:
            return (
                DropTable.from_data(response["droptables"]),
                [
                    ItemFull.from_data(item)
                    for item in response["include"]["item"]["items_in_set"]
                ],
            )
        return from_data(DropTable, response["droptables"])
