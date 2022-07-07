import aiohttp
from pytenno.models.auctions import RivenAuction
from pytenno.models.enums import Platform
from pytenno.models.locations import Location
from pytenno.models.missions import NPC, PartialMission
from pytenno.models.users import CurrentUser
from types import NoneType, TracebackType
from typing import Literal, Optional, Type, Union, overload

from ._backends import (
    AuctionsBackend,
    AuthBackend,
    ItemBackend,
    LichBackend,
    MiscBackend,
    RivenBackend,
)
from .constants import VALID_LANGUAGES
from .models.auctions import (
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

        self.auctions: Auctions
        self.auth: Auth
        self.items: Items
        self.liches: Liches
        self.misc: Misc
        self.rivens: Rivens

    async def __aenter__(self):
        headers = {
            "Authorization": "JWT",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "language": self._language,
            "platform": self._platform.name,
        }
        self._session = aiohttp.ClientSession(headers=headers)

        self.auctions = Auctions(self._session)
        self.auth = Auth(self._session)
        self.items = Items(self._session)
        self.liches = Liches(self._session)
        self.misc = Misc(self._session)
        self.rivens = Rivens(self._session)
        return self

    async def __aexit__(
        self,
        exctype: Optional[Type[BaseException]],
        excinst: Optional[BaseException],
        exctb: Optional[TracebackType],
    ) -> bool:
        await self._session.close()
        return False


class Auctions(AuctionsBackend):
    async def create_auction(
        self,
        item: Union[RivenAuction, LichAuction, KubrowAuction],
        note: str,
        starting_price: int,
        buyout_price: int,
        minimal_reputation: int = 0,
        minimal_increment: int = 1,
        private: bool = False,
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


class Auth(AuthBackend):
    async def login(
        self,
        email: str,
        password: str,
    ) -> CurrentUser:
        return await self._login(email, password)


class Items(ItemBackend):
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


class Liches(LichBackend):
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


class Rivens(RivenBackend):
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

