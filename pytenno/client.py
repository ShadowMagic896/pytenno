import aiohttp
from pytenno.models.auctions import RivenAuction
from pytenno.models.enums import Element, Platform, Polarity
from pytenno.models.locations import Location
from pytenno.models.missions import NPC, PartialMission
from pytenno.models.users import CurrentUser
from types import TracebackType
from typing import Literal, Optional, Type, Union, overload

from ._backends import (
    AuctionEntriesBackend,
    AuctionsBackend,
    AuthBackend,
    ItemsBackend,
    LichesBackend,
    MiscBackend,
    RivensBackend,
)
from .constants import VALID_LANGUAGES
from .models.auctions import (
    AuctionEntry,
    AuctionEntryExpanded,
    KubrowAuction,
    LichAuction,
    RivenAuction,
)
from .models.droptable import DropTable
from .models.items import ItemFull, ItemShort
from .models.liches import LichEphemera, LichQuirk, LichWeapon
from .models.orders import OrderRow
from .models.rivens import RivenAttribute, RivenItem


class PyTenno:
    def __init__(
        self, language: VALID_LANGUAGES = "en", platform: Platform = Platform.pc
    ) -> None:
        self._language = language
        self._platform = platform

        self._session: aiohttp.ClientSession = None

        self.AuctionEntries: AuctionEntries
        self.Auctions: Auctions
        self.Auth: Auth
        self.Items: Items
        self.Liches: Liches
        self.Misc: Misc
        self.Rivens: Rivens

    async def __aenter__(self):
        headers = {
            "Authorization": "JWT",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "language": self._language,
            "platform": self._platform.name,
        }
        self._session = aiohttp.ClientSession(headers=headers)

        self.AuctionEntries = AuctionEntries(self._session)
        self.Auctions = Auctions(self._session)
        self.Auth = Auth(self._session)
        self.Items = Items(self._session)
        self.Liches = Liches(self._session)
        self.Misc = Misc(self._session)
        self.Rivens = Rivens(self._session)
        return self

    async def __aexit__(
        self,
        exctype: Optional[Type[BaseException]],
        excinst: Optional[BaseException],
        exctb: Optional[TracebackType],
    ) -> bool:
        await self._session.close()
        return False


class AuctionEntries(AuctionEntriesBackend):
    async def get_by_id(self, auction_id: str) -> AuctionEntryExpanded:
        return await self._get_by_id(auction_id)

    async def get_bids_by_id(self, auction_id: str) -> AuctionEntryExpanded:
        return await self._get_bids_by_id(auction_id)


class Auctions(AuctionsBackend):
    async def create_auction(
        self,
        item: Union[RivenAuction, LichAuction, KubrowAuction],
        note: str,
        starting_price: int,
        buyout_price: int,
        minimal_reputation: Optional[int] = 0,
        minimal_increment: Optional[int] = 1,
        private: Optional[bool] = False,
    ) -> list[AuctionEntryExpanded]:
        return await self._create_auction(
            item,
            note,
            starting_price,
            buyout_price,
            minimal_reputation,
            minimal_increment,
            private,
        )

    async def find_riven_auctions(
        self,
        *,
        platform: Platform = Platform.pc,
        weapon_url_name: str,
        mastery_rank_min: int = None,
        mastery_rank_max: int = None,
        re_rolls_min: int = None,
        re_rolls_max: int = None,
        positive_stats: str = None,
        negative_stats: str = None,
        polarity: Polarity = Polarity.any,
        mod_rank: Literal["any", "maxed"] = None,
        sort_by: Optional[
            Literal[
                "price_desc", "price_asc", "positive_attr_desc", "positive_attr_asc"
            ]
        ] = None,
        operation: Optional[Literal["anyOf", "allOf"]] = None,
        buyout_policy: Optional[Literal["with", "direct"]] = None,
    ) -> list[AuctionEntryExpanded]:
        return await self._find_riven_auctions(
            platform=platform,
            weapon_url_name=weapon_url_name,
            mastery_rank_min=mastery_rank_min,
            mastery_rank_max=mastery_rank_max,
            re_rolls_min=re_rolls_min,
            re_rolls_max=re_rolls_max,
            positive_stats=positive_stats,
            negative_stats=negative_stats,
            polarity=polarity,
            mod_rank=mod_rank,
            sort_by=sort_by,
            operation=operation,
            buyout_policy=buyout_policy,
        )

    async def find_lich_auctions(
        self,
        *,
        weapon_url_name: str,
        platform: Platform = Platform.pc,
        element: Optional[Element] = None,
        ephemera: Optional[bool] = None,
        damage_min: Optional[int] = None,
        damage_max: Optional[int] = None,
        quirk_url_name: Optional[str] = None,
        sort_by: Optional[
            Literal[
                "price_desc", "price_asc", "positive_attr_desc", "positive_attr_asc"
            ]
        ] = "price_desc",
        buyout_policy: Optional[Literal["with", "direct"]] = None,
    ) -> list[AuctionEntryExpanded]:
        return await self._find_lich_auctions(
            platform=platform,
            weapon_url_name=weapon_url_name,
            element=element,
            ephemera=ephemera,
            damage_min=damage_min,
            damage_max=damage_max,
            quirk_url_name=quirk_url_name,
            sort_by=sort_by,
            buyout_policy=buyout_policy,
        )


class Auth(AuthBackend):
    async def login(
        self,
        email: str,
        password: str,
    ) -> CurrentUser:
        return await self._login(email, password)

    async def register(
        self,
        email: str,
        password: str,
        region: Optional[VALID_LANGUAGES] = "en",
        device_id: Optional[str] = None,
        recaptcha: Optional[str] = None,
    ) -> CurrentUser:
        return await self._register(email, password, region, device_id, recaptcha)

    async def recover(self, email: str) -> None:
        return await self._recover(email)


class Items(ItemsBackend):
    """
    Provides all information about common items data models.
    """

    async def get_items(self, language: VALID_LANGUAGES = "en") -> list[ItemShort]:
        """
        Returns all available items
        """
        return await self._get_items(language)

    @overload
    async def get_droptable(
        self,
        item_name: str,
        include_items: Literal[True],
        language: VALID_LANGUAGES = "en",
    ) -> tuple[list[DropTable], list[ItemFull]]:
        ...

    @overload
    async def get_droptable(
        self,
        item_name: str,
        include_items: Literal[False],
        language: VALID_LANGUAGES = "en",
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
        return await self._get_item(item_name, platform)

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
        return await self._get_orders(item_name, include_items, platform)

    @overload
    async def get_droptable(
        self,
        item_name: str,
        include_items: Literal[False],
        language: VALID_LANGUAGES = "en",
    ) -> DropTable:
        ...

    @overload
    async def get_droptable(
        self,
        item_name: str,
        include_items: Literal[True],
        language: VALID_LANGUAGES = "en",
    ) -> tuple[DropTable, list[ItemFull]]:
        ...

    async def get_droptable(
        self,
        item_name: str,
        include_items: bool,
        language: VALID_LANGUAGES = "en",
    ):
        raise Exception(
            "The API on warframe.market for this feature is currently nonfunctional"
        )


class Liches(LichesBackend):
    """
    Provides all information about lich data models.
    """

    async def get_weapons(self, language: VALID_LANGUAGES = "en") -> list[LichWeapon]:
        return await self._get_weapons(language)

    async def get_ephemeras(
        self, language: VALID_LANGUAGES = "en"
    ) -> list[LichEphemera]:
        return await self._get_ephemeras(language)

    async def get_quirks(self, language: VALID_LANGUAGES = "en") -> list[LichQuirk]:
        return await self._get_quirks(language)


class Rivens(RivensBackend):
    """
    Provides all information about riven data models.
    """

    async def get_items(self, language: VALID_LANGUAGES = "en") -> list[RivenItem]:
        return await self._get_riven_items(language)

    async def get_attributes(
        self, language: VALID_LANGUAGES = "en"
    ) -> list[RivenAttribute]:
        return await self._get_riven_attributes(language)


class Misc(MiscBackend):
    """
    Additional miscellaneous endpoints
    """

    async def get_locations(self, language: VALID_LANGUAGES = "en") -> list[Location]:
        # nonfunctional
        return await self._get_locations(language)

    async def get_npcs(self, language: VALID_LANGUAGES = "en") -> list[NPC]:
        # nonfunctional
        return await self._get_npcs(language)

    async def get_missions(
        self, language: VALID_LANGUAGES = "en"
    ) -> list[PartialMission]:
        # nonfunctional
        return await self._get_missions(language)
