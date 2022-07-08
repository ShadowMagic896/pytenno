import aiohttp
from typing import Any, Literal, Union

from .constants import API_ROOT, VALID_LANGUAGES
from .models.auctions import (
    AuctionEntry,
    AuctionEntryExpanded,
    KubrowAuction,
    LichAuction,
    RivenAuction,
)
from .models.droptable import DropTable
from .models.enums import Element, Platform, Polarity
from .models.items import ItemFull, ItemShort
from .models.liches import LichEphemera, LichQuirk, LichWeapon
from .models.locations import Location
from .models.missions import DroptableNPC, PartialMission
from .models.orders import OrderRow
from .models.rivens import RivenAttribute, RivenItem
from .models.users import CurrentUser
from .utils import _raise_error_code, format_name, from_data


class PyTennoBackend:
    def __init__(
        self, session: aiohttp.ClientSession, silenced: list[Exception]
    ) -> None:
        self._session = session
        self.silenced = silenced

    async def _request(self, url: str, **kwargs) -> dict[str, str | int | dict | list] | None:
        url = f"{API_ROOT}{url}"
        mode = getattr(self._session, kwargs.pop("method", "get"))
        response: aiohttp.ClientResponse = await mode(url, **kwargs)
        if response.status != 200:
            return _raise_error_code(response, self.silenced)
        return await response.json()


class BackendAdapter:
    def __init__(self, backend: PyTennoBackend) -> None:
        self._backend = backend


class AuctionEntriesBackend(BackendAdapter):
    async def _get_by_id(
        self,
        auction_id: str,
    ):
        data = await self._backend._request(f"/auctions/entry/{auction_id}")
        return from_data(AuctionEntryExpanded, data)

    async def _get_bids_by_id(self, auction_id: str):
        data = await self._backend._request(f"/auctions/entry/{auction_id}/bids")
        return from_data(AuctionEntryExpanded, data)


class AuctionsBackend(BackendAdapter):
    async def _create_auction(
        self,
        item: Union[RivenAuction, LichAuction, KubrowAuction],
        note: str,
        starting_price: int,
        buyout_price: int,
        minimal_reputation: int = 0,
        minimal_increment: int = 1,
        private: bool = False,
    ):
        url = "/auctions/create"
        attributes = [
            {
                [
                    {
                        "positive": attribute.positive,
                        "value": attribute.value,
                        "url": attribute.url_name,
                    }
                ]
                for attribute in item.attributes
            }
        ]
        data = {
            "note": note,
            "starting_price": starting_price,
            "buyout_price": buyout_price,
            "minimal_reputation": minimal_reputation,
            "minimal_increment": minimal_increment,
            "private": private,
            "item": {
                "type": item.type.name.lower(),
                "attributes": attributes,
                "name": item.name.lower(),
                "mastery_level": item.mastery_level,
                "re_rolls": item.re_rolls,
                "weapon_url_name": item.weapon_url_name,
                "polarity": item.polarity.name.lower(),
                "mod_rank": item.mod_rank,
            },
        }

        response = await self._backend._request(url, method="post", data=str(data))
        return from_data(AuctionEntry, response["payload"]["auction"])

    async def _find_riven_auctions(
        self,
        *,
        weapon_url_name: str,
        platform: Platform,
        buyout_policy: Literal["with", "direct"] | None = None,
        mastery_rank_min: int | None = None,
        mastery_rank_max: int | None = None,
        re_rolls_min: int | None = None,
        re_rolls_max: int | None = None,
        positive_stats: list[str] | None = None,
        negative_stats: list[str] | None = None,
        polarity: Polarity = Polarity.any,
        mod_rank: Literal["any", "maxed"] | None = None,
        sort_by: Literal[
            "price_desc", "price_asc", "positive_attr_desc", "positive_attr_asc"
        ]
        | None = None,
        operation: Literal["anyOf", "allOf"] | None = None,
    ):
        url = (
            f"/auctions/search?type=riven&"
            + (
                f"weapon_url_name={weapon_url_name}&"
                if weapon_url_name is not None
                else ""
            )
            + (
                f"mastery_rank_min={mastery_rank_min}&"
                if mastery_rank_min is not None
                else ""
            )
            + (
                f"mastery_rank_max={mastery_rank_max}&"
                if mastery_rank_max is not None
                else ""
            )
            + (f"re_rolls_min={re_rolls_min}&" if re_rolls_min is not None else "")
            + (f"re_rolls_max={re_rolls_max}&" if re_rolls_max is not None else "")
            + (
                f"positive_stats={','.join([str(s) for s in positive_stats])}&"
                if positive_stats is not None
                else ""
            )
            + (
                f"negative_stats={','.join([str(s) for s in negative_stats])}&"
                if negative_stats is not None
                else ""
            )
            + f"polarity={polarity}&"
            + (f"mod_rank={mod_rank}&" if mod_rank is not None else "")
            + (f"sort_by={sort_by}&" if sort_by is not None else "")
            + (f"operation={operation}&" if operation is not None else "")
            + (f"buyout_policy={buyout_policy}" if buyout_policy is not None else "")
        ).strip("&")

        headers = {"Platform": platform.name.lower()}
        response = await self._backend._request(url, headers=headers)

        return [
            from_data(AuctionEntryExpanded, node)
            for node in response["payload"]["auctions"]
        ]

    async def _find_lich_auctions(
        self,
        *,
        platform: Platform,
        weapon_url_name: str,
        element: Element,
        ephemera: bool,
        damage_min: int,
        damage_max: int,
        quirk_url_name: str,
        sort_by: Literal[
            "price_desc", "price_asc", "positive_attr_desc", "positive_attr_asc"
        ] = "price_desc",
        buyout_policy: Literal["with", "direct", "all"] = "all",
    ):
        url = (
            f"/auctions/search?type=lich&"
            + f"weapon_url_name={format_name(weapon_url_name)}&"
            + (f"element={element.name.lower()}&" if element is not None else "")
            + (f"ephemera={ephemera}&" if ephemera is not None else "")
            + (f"damage_min={damage_min}&" if damage_min is not None else "")
            + (f"damage_max={damage_max}&" if damage_max is not None else "")
            + (f"quirk={quirk_url_name}&" if quirk_url_name is not None else "")
            + (f"sort_by={sort_by}&" if sort_by is not None else "")
            + (f"buyout_policy={buyout_policy}" if buyout_policy is not None else "")
        ).strip("&")
        headers = {"Platform": platform.name.lower()}
        response = await self._backend._request(url, headers=headers)

        return [
            from_data(AuctionEntryExpanded, node)
            for node in response["payload"]["auctions"]
        ]


class AuthBackend(BackendAdapter):
    async def _login(
        self,
        email: str,
        password: str,
        device_id: str,
    ):
        url = "/auth/signin"
        data = {
            "auth_type": "header",
            "email": email,
            "password": password,
            "device_id": device_id,
        }
        response = await self._backend._request(url, json=data, method="post")
        return from_data(CurrentUser, response["payload"]["user"])

    async def _register(
        self, email: str, password: str, region: str, device_id: str, recaptcha: str
    ):
        url = "/auth/registration"
        data = {
            "auth_type": "header",
            "email": email,
            "password": password,
            "region": region,
            "device_id": device_id,
            "recaptcha": recaptcha,
        }
        response = await self._backend._request(url, json=data, method="post")
        return from_data(CurrentUser, response)

    async def _restore(self, email: str):
        url = "/auth/restore"
        data = {
            "email": email,
        }
        await self._backend._request(url, json=data, method="post")
        return None


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


class LichesBackend(BackendAdapter):
    async def _get_weapons(self, language):
        url = "/lich/weapons"
        headers = {"Language": language}
        response = await self._backend._request(url, headers=headers)
        return [from_data(LichWeapon, node) for node in response["payload"]["weapons"]]

    async def _get_ephemeras(self, language):
        url = "/lich/ephemeras"
        headers = {"Language": language}
        response = await self._backend._request(url, headers=headers)
        return [
            from_data(LichEphemera, node) for node in response["payload"]["ephemeras"]
        ]

    async def _get_quirks(self, language):
        url = "/lich/quirks"
        headers = {"Language": language}
        response = await self._backend._request(url, headers=headers)
        return [from_data(LichQuirk, node) for node in response["payload"]["quirks"]]


class RivensBackend(BackendAdapter):
    async def _get_riven_items(self, language):
        url = "/riven/items"
        headers = {"Language": language}
        response = await self._backend._request(url, headers=headers)
        return [from_data(RivenItem, node) for node in response["payload"]["items"]]

    async def _get_riven_attributes(self, language):
        url = "/riven/attributes"
        headers = {"Language": language}
        response = await self._backend._request(url, headers=headers)
        return [
            from_data(RivenAttribute, node)
            for node in response["payload"]["attributes"]
        ]


class MiscBackend(BackendAdapter):
    async def _get_locations(self, language):
        url = "/misc/locations"
        headers = {"Language": language}
        response = await self._backend._request(url, headers=headers)
        return [from_data(Location, node) for node in response["payload"]["locations"]]

    async def _get_npcs(self, language):
        url = "/misc/npc"
        headers = {"Language": language}
        response = await self._backend._request(url, headers=headers)
        return [from_data(DroptableNPC, node) for node in response["payload"]["npc"]]

    async def _get_missions(self, language):
        url = "/misc/missions"
        headers = {"Language": language}
        response = await self._backend._request(url, headers=headers)
        return [
            from_data(PartialMission, node) for node in response["payload"]["missions"]
        ]


class IgnoredError(Exception):
    def __init__(self, exception: Exception, response: dict[str, Any]):
        self.exception = exception
        self.response = response

    def __str__(self):
        return self.exception.__str__()

    def __bool__(self):
        return False

    def __repr__(self):
        return self.exception.__str__()

    def __eq__(self, other):
        return isinstance(other, IgnoredError)

    def __hash__(self):
        return hash(self.exception)

    def __getitem__(self, key):
        return self.response[key]

    def __setitem__(self, key, value):
        self.response[key] = value
