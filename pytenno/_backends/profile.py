from pytenno.models.enums import OrderType, Platform
from pytenno.models.items import ItemInOrder, ItemFull
from pytenno.models.orders import OrderCommon, OrderCreated, OrderRow
from pytenno.utils import from_data
from .core import BackendAdapter

class ProfileBackend(BackendAdapter):
    async def _create_order(self, language, data: dict):
        url = "/profile/orders"
        headers = {"Language": language}
        response = await self._backend._request(url, headers=headers, data=data)
        order = response["payload"]["order"]
        return from_data(OrderCreated, order)