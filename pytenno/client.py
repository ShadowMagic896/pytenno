import aiohttp
from pytenno.models.auctions import RivenAuction
from pytenno.models.enums import Element, Platform, Polarity, RivenStat
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
    PyTennoBackend,
    RivensBackend,
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
        self,
        language: VALID_LANGUAGES = "en",
        platform: Platform = Platform.pc,
        silenced_errors: list[Exception] = [],
    ) -> None:
        self._language = language
        self._platform = platform

        self._session: aiohttp.ClientSession = None
        self._silenced = silenced_errors

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
        backend = PyTennoBackend(self._session, self._silenced)

        self.AuctionEntries = AuctionEntries(backend)
        self.Auctions = Auctions(backend)
        self.Auth = Auth(backend)
        self.Items = Items(backend)
        self.Liches = Liches(backend)
        self.Misc = Misc(backend)
        self.Rivens = Rivens(backend)
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
        """Gets a specific auction entry by ID.

        Parameters
        ----------
        `auction_id`: :class:`str`
            The ID of the auction entry to get.

        Returns
        -------
        :class:`AuctionEntryExpanded`
        """
        return await self._get_by_id(auction_id)

    async def get_bids_by_id(self, auction_id: str) -> AuctionEntryExpanded:
        """Gets all bids for a specific auction entry by ID.

        Parameters
        ----------
        `auction_id`: :class:`str`
            The ID of the auction entry to get bids for.

        Returns
        -------
        :class:`AuctionEntryExpanded`
        """
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
        weapon_url_name: str,
        platform: Platform = Platform.pc,
        mastery_rank_min: int = None,
        mastery_rank_max: int = None,
        re_rolls_min: int = None,
        re_rolls_max: int = None,
        positive_stats: list[RivenStat] = None,
        negative_stats: list[RivenStat] = None,
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
        """Finds all riven auctions that match the given criteria.
        
        Parameters
        ----------
        `weapon_url_name`: :class:`str`
            The URL name of the weapon to search for.
        `platform`: :class:`Platform`
            The platform to search for riven auctions on. Default: :class:`Platform.pc`.
        `mastery_rank_min`: :class:`int`
            The minimum mastery rank of the riven. Default: :class:`None`.
        `mastery_rank_max`: :class:`int`
            The maximum mastery rank of the riven. Default: :class:`None`.
        `re_rolls_min`: :class:`int`
            The minimum number of re-rolls of the riven. Default: :class:`None`.
        `re_rolls_max`: :class:`int`
            The maximum number of re-rolls of the riven. Default: :class:`None`.
        `positive_stats`: :class:`list` of :class:`RivenStat`
            Restricts the riven to have the given positive stats. Maximum amount is 3. Default: :class:`None`.
        `negative_stats`: :class:`list` of :class:`RivenStat`
            Restricts the riven to have the given negative stats. Maximum amount is 3. Default: :class:`None`.
        `polarity`: :class:`Polarity`
            The polarity of the riven. Default: :class:`Polarity.any`.

        Returns
        -------
        :class:`list`[:class:`AuctionEntryExpanded` ]   
        """
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
        """Finds all lich auctions that match the given criteria.

        Parameters
        ----------
        `weapon_url_name`: :class:`str`
            The URL name of the weapon to search for.
        `platform`: :class:`Platform`
            The platform to search for lich auctions on. Default: :class:`Platform.pc`.
        `element`: :class:`Element`
            The element of the lich. Default: :class:`None`.
        `ephemera`: :class:`bool`
            Whether the lich is ephemeral. Default: :class:`None`.
        `damage_min`: :class:`int`
            The minimum damage of the lich. Default: :class:`None`.
        `damage_max`: :class:`int`
            The maximum damage of the lich. Default: :class:`None`.
        `quirk_url_name`: :class:`str`
            The URL name of the quirk of the lich. Default: :class:`None`.
        `sort_by`: :class:`Literal`
            The sort order of the results. Default: `"price_desc"`.
        `buyout_policy`: :class:`Literal`
            The buyout policy of the results. Default: :class:`None`.
        
        Returns
        -------
        :class:`list`[:class:`AuctionEntryExpanded`]
        """
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
        """Logs in the user with the given credentials.
        
        Parameters
        ----------
        `email`: :class:`str`
            The email of the user.
        `password`: :class:`str`
            The password of the user.
        
        Returns
        -------
        :class:`CurrentUser`
        """
        return await self._login(email, password)

    async def register(
        self,
        email: str,
        password: str,
        region: Optional[VALID_LANGUAGES] = "en",
        device_id: Optional[str] = None,
        recaptcha: Optional[str] = None,
    ) -> CurrentUser:
        """Registers a new user with the given credentials.
        
        Parameters
        ----------
        `email`: :class:`str`
            The email of the user.
        `password`: :class:`str`
            The password of the user.
        `region`: :class:`VALID_LANGUAGES`
            The region of the user. Default: `"en"`.
        `device_id`: :class:`str`
            The device ID of the user, used to identify devices between sessions. Default: :class:`None`.
        `recaptcha`: :class:`str`
            The Google recaptcha response of the user. Default: :class:`None`.
        
        Returns
        -------
        :class:`CurrentUser`
        """
        return await self._register(email, password, region, device_id, recaptcha)

    async def recover(self, email: str) -> None:
        """"Sends the user a recovery email.
        
        Parameters
        ----------
        email: :class:`str`
            The email of the user.
        
        Returns
        -------
        :class:`None`
        """
        return await self._recover(email)


class Items(ItemsBackend):
    async def get_items(self, language: VALID_LANGUAGES = "en") -> list[ItemShort]:
        """Gets all items.
        
        Parameters
        ----------
        `language`: :class:`VALID_LANGUAGES`
            The language of the items. Default: `"en"`.
        
        Returns
        -------
        :class:`list`[:class:`ItemShort`]
        """
        return await self._get_items(language)

    async def get_item(
        self,
        item_name: str,
        platform: Optional[Platform] = Platform.pc,
    ) -> list[ItemFull]:
        """Gets the item with the given name, as well as related items (such as items of the same set).
        
        Parameters
        ----------
        `item_name`: :class:`str`
            The name of the item.
        `platform`: :class:`Platform`
            The platform of the item. Default: :class:`Platform.pc`.

        Returns
        -------
        :class:`list`[:class:`ItemFull`]
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
        `item_name`: :class:`str`
            The name of the item.
        `include_items`: :class:`bool`
            Whether to include information about the item requested.
        `platform`: :class:`Platform`
            The platform of the item. Default: :class:`Platform.pc`.
        
        Returns
        -------
        :class:`list`[:class:`OrderRow`] | :class:`tuple`(:class:`list`[:class:`OrderRow`], :class:`list`[:class:`ItemFull`])
        """
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
        """Gets the droptable of the given item.
        
        Parameters
        ----------
        `item_name`: :class:`str`
            The name of the item.
        `include_items`: :class:`bool`
            Whether to include information about the item requested.
        `language`: :class:`VALID_LANGUAGES`
            The language of the droptable. Default: `"en"`.
        
        Returns
        -------
        :class:`DropTable` | :class:`tuple`(:class:`DropTable`, :class:`list`[:class:`ItemFull`])
        """
        raise Exception(
            "The API on warframe.market for this feature is currently nonfunctional"
        )


class Liches(LichesBackend):
    async def get_weapons(self, language: VALID_LANGUAGES = "en") -> list[LichWeapon]:
        """Gets all weapons.
        
        Parameters
        ----------
        `language`: :class:`VALID_LANGUAGES`
            The language of the weapons. Default: `"en"`.
        
        Returns
        -------
        :class:`list`[:class:`LichWeapon`]
        """
        return await self._get_weapons(language)

    async def get_ephemeras(
        self, language: VALID_LANGUAGES = "en"
    ) -> list[LichEphemera]:
        """Gets all lich ephemeras.
        
        Parameters
        ----------
        `language`: :class:`VALID_LANGUAGES`
            The language of the ephemeras. Default: `"en"`.
        
        Returns
        -------
        :class:`list`[:class:`LichEphemera`]
        """
        return await self._get_ephemeras(language)

    async def get_quirks(self, language: VALID_LANGUAGES = "en") -> list[LichQuirk]:
        """Gets all lich quirks.
        
        Parameters
        ----------
        `language`: :class:`VALID_LANGUAGES`
            The language of the quirks. Default: `"en"`.
        
        Returns
        -------
        :class:`list`[:class:`LichQuirk`]"""
        return await self._get_quirks(language)


class Rivens(RivensBackend):
    async def get_riven_items(self, language: VALID_LANGUAGES = "en") -> list[RivenItem]:
        """Gets a list of all riven-equippable items.
    
        Parameters
        ----------
        `language`: :class:`VALID_LANGUAGES`
            The language of the riven items. Default: `"en"`.
        
        Returns
        -------
        :class:`list`[:class:`RivenItem`]
        """
        return await self._get_riven_items(language)

    async def get_attributes(
        self, language: VALID_LANGUAGES = "en"
    ) -> list[RivenAttribute]:
        """Gets a list of all riven attributes.
        
        Parameters
        ----------
        `language`: :class:`VALID_LANGUAGES`
            The language of the riven attributes. Default: `"en"`.
        
        Returns
        -------
        :class:`list`[:class:`RivenAttribute`]
        """
        return await self._get_riven_attributes(language)


class Misc(MiscBackend):
    async def get_locations(self, language: VALID_LANGUAGES = "en") -> list[Location]:
        """Gets a list of all locations.

        Parameters
        ----------
        `language`: :class:`VALID_LANGUAGES`
            The language of the locations. Default: `"en"`.
        
        Returns
        -------
        :class:`list`[:class:`Location`]
        """
        return await self._get_locations(language)

    async def get_npcs(self, language: VALID_LANGUAGES = "en") -> list[NPC]:
        """Gets a list of all NPCs.
        
        Parameters
        ----------
        `language`: :class:`VALID_LANGUAGES`
            The language of the NPCs. Default: `"en"`.
        
        Returns
        -------
        :class:`list`[:class:`NPC`]
        """
        return await self._get_npcs(language)

    async def get_missions(
        self, language: VALID_LANGUAGES = "en"
    ) -> list[PartialMission]:
        """Gets a list of all missions.
        
        Parameters
        ----------
        `language`: :class:`VALID_LANGUAGES`
            The language of the missions. Default: `"en"`.
        
        Returns
        -------
        :class:`list`[:class:`PartialMission`]"""
        return await self._get_missions(language)
