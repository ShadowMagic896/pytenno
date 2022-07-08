from typing import Literal, Optional, Union, overload
from .constants import VALID_LANGUAGES
from .models.auctions import AuctionEntryExpanded, KubrowAuction, LichAuction, RivenAuction
from .models.droptable import DropTable
from .models.enums import Element, Platform, Polarity, RivenStat
from .models.items import ItemFull, ItemShort
from .models.liches import LichEphemera, LichQuirk, LichWeapon
from .models.locations import Location
from .models.missions import DroptableNPC, PartialMission
from .models.orders import OrderRow
from .models.rivens import RivenAttribute, RivenItem
from .models.users import CurrentUser
from .client_backends import (AuctionEntriesBackend, AuctionsBackend, AuthBackend, ItemsBackend, LichesBackend, MiscBackend, RivensBackend)


class AuctionEntries(AuctionEntriesBackend):
    """A class for getting information about auction entries by ID."""

    async def get_by_id(self, auction_id: str) -> AuctionEntryExpanded:
        """Gets a specific auction entry by ID.

        Parameters
        ----------
        `auction_id`: :class:`str`
            The ID of the auction entry to get.

        Returns
        -------
        :class:`AuctionEntryExpanded`

        Examples
        --------
        >>> async with PyTenno() as tenno:
        >>>     auction = await tenno.AuctionEntries.get_by_id("...")
        >>>     print(auction.owner.ingame_name, auction.platinum)
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

        Examples
        --------
        >>> async with PyTenno() as tenno:
        >>>     auction = await tenno.AuctionEntries.get_bids_by_id("...")
        >>>     print(auction.owner.ingame_name, auction.platinum)
        """
        return await self._get_bids_by_id(auction_id)


class Auctions(AuctionsBackend):
    """A class for creating and searching for auctions with certain criteria."""

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
        """Creates a new auction.

        Parameters
        ----------
        `item`: :class:`RivenAuction`, :class:`LichAuction`, :class:`KubrowAuction`
            The item to auction.
        `note`: :class:`str`
            The note to put on the auction.
        `starting_price`: :class:`int`
            The starting price of the auction. (In platinum)
        `buyout_price`: :class:`int`
            The buyout price of the auction. (In platinum)
        `minimal_reputation`: :class:`int`, optional
            The minimmum reputation a user must have to bid on the auction.
        `minimal_increment`: :class:`int`, optional
            The minimum amount between bids. (In platinum)
        `private`: :class:`bool`, optional
            Whether the auction is private or not. If it is private, you can set it to public in the auction settings in the web interface.

        Returns
        -------
        :class:`list`[:class:`AuctionEntryExpanded`]

        Raises
        ------
        :class:`ValueError`
            If the starting price is higher than the buyout price.
        :class:`ValueError`
            If the minimal increment is less than 1.

        Examples
        --------
        >>> async with PyTenno() as tenno:
        >>>     auction = await tenno.Auctions.create_auction(
        >>>         item=RivenAuction(...),
        >>>         note="...",
        >>>         starting_price=100,
        >>>         buyout_price=200,
        >>>         minimal_reputation=0,
        >>>         minimal_increment=50
        >>>     )
        >>>     print(auction.owner.ingame_name, auction.platinum)
        """
        if starting_price > buyout_price:
            raise ValueError("Starting price cannot be higher than buyout price.")
        if minimal_increment < 1:
            raise ValueError("Minimal increment cannot be less than 1.")

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

        Raises
        ------
        :class:`ValueError`
            If the amount of positive stats is greater than 3.
        :class:`ValueError`
            If the amount of negative stats is greater than 3.
        :class:`ValueError`
            If the mastery rank min is greater than the mastery rank max.
        :class:`ValueError`
            If the re-rolls min is greater than the re-rolls max.
        :class:`ValueError`
            If the mastery rank min is less than 0.
        :class:`ValueError`
            If the re-rolls min is less than 0.

        Examples
        --------
        >>> auctions = await tenno.auctions.find_riven_auctions(
        >>>     weapon_url_name="shedu",
        >>>     mastery_rank_max=9,
        >>>     re_rolls_max=10
        >>> )
        >>> for auction in auctions:
        >>>     print(auction.id)
        >>>     print(auction.item.element.name)
        """
        if positive_stats is not None and len(positive_stats) > 3:
            raise ValueError("The amount of positive stats cannot be greater than 3.")
        if negative_stats is not None and len(negative_stats) > 3:
            raise ValueError("The amount of negative stats cannot be greater than 3.")
        if mastery_rank_min is not None and mastery_rank_min > mastery_rank_max:
            raise ValueError(
                "The mastery rank min cannot be greater than the mastery rank max."
            )
        if re_rolls_min is not None and re_rolls_min > re_rolls_max:
            raise ValueError(
                "The re-rolls min cannot be greater than the re-rolls max."
            )
        if mastery_rank_min is not None and mastery_rank_min < 0:
            raise ValueError("The mastery rank min cannot be less than 0.")
        if re_rolls_min is not None and re_rolls_min < 0:
            raise ValueError("The re-rolls min cannot be less than 0.")

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

        Raises
        ------
        :class:`ValueError`
            If the damage min is greater than the damage max.
        :class:`ValueError`
            If the damage min is less than 0.
        :class:`ValueError`
            If the damage max is less than 0.

        Examples
        --------
        >>> async with PyTenno() as tenno:
        >>>     auctions = await tenno.auctions.find_lich_auctions(
        >>>         weapon_url_name="kuva_bramma",
        >>>         damage_min=20,
        >>>         element=Element.toxin,
        >>>     )
        >>>     for auction in auctions:
        >>>         print(auction.id, auction.owner.ingame_name)
        """
        if damage_min is not None and damage_min > damage_max:
            raise ValueError("The damage min cannot be greater than the damage max.")
        if damage_min is not None and damage_min < 0:
            raise ValueError("The damage min cannot be less than 0.")
        if damage_max is not None and damage_max < 0:
            raise ValueError("The damage max cannot be less than 0.")

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
        *,
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

        Examples
        --------
        >>> async with PyTenno() as tenno:
        >>>     current_user = await tenno.auth.login(
        >>>         email="example@nothing.co"
        >>>         password="password"
        >>>     )
        >>>     print(current_user.ingame_name)
        """
        return await self._login(email, password)

    async def register(
        self,
        *,
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

        Examples
        --------
        >>> async with PyTenno() as pytenno:
        >>>     email = "example@nothing.co"
        >>>     password = "password"
        >>>     region = "en"
        >>>     current_user = await pytenno.auth.register(email, password, region)
        >>>     print(current_user.ingame_name)

        """
        return await self._register(email, password, region, device_id, recaptcha)

    async def recover(self, email: str) -> None:
        """ "Sends the user a recovery email.

        Parameters
        ----------
        email: :class:`str`
            The email of the user.

        Returns
        -------
        :class:`None`

        Examples
        --------
        >>> async with PyTenno() as pytenno:
        >>>     email = "example@nothing.co"
        >>>     await pytenno.auth.recover(email=email)
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

        Examples
        --------
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
        `item_name`: :class:`str`
            The name of the item.
        `platform`: :class:`Platform`
            The platform of the item. Default: :class:`Platform.pc`.

        Returns
        -------
        :class:`list`[:class:`ItemFull`]

        Examples
        --------
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
        `item_name`: :class:`str`
            The name of the item.
        `include_items`: :class:`bool`
            Whether to include information about the item requested.
        `platform`: :class:`Platform`
            The platform of the item. Default: :class:`Platform.pc`.

        Returns
        -------
        :class:`list`[:class:`OrderRow`] | :class:`tuple`(:class:`list`[:class:`OrderRow`], :class:`list`[:class:`ItemFull`])

        Examples
        --------
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

        Examples
        --------
        >>> async with PyTenno() as pytenno:
        >>>     droptable, items = await pytenno.items.get_droptable("kuva_bramma", include_items=True)
        >>>     print(droptable.relics, droptable.missions)
        >>>     for item in items:
        >>>         print(item.url_name)

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

        Examples
        --------
        >>> async with PyTenno() as pytenno:
        >>>     weapons = await pytenno.liches.get_weapons()
        >>>     for weapon in weapons:
        >>>         print(weapon.url_name)
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

        Examples
        --------
        >>> async with PyTenno() as pytenno:
        >>>     ephemeras = await pytenno.liches.get_ephemeras()
        >>>     for ephemera in ephemeras:
        >>>         print(ephemera.url_name)
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
        :class:`list`[:class:`LichQuirk`]

        Examples
        --------
        >>> async with PyTenno() as pytenno:
        >>>     quirks = await pytenno.liches.get_quirks()
        >>>     for quirk in quirks:
        >>>         print(quirk.url_name)
        """
        return await self._get_quirks(language)


class Rivens(RivensBackend):
    async def get_riven_items(
        self, language: VALID_LANGUAGES = "en"
    ) -> list[RivenItem]:
        """Gets a list of all riven-equippable items.

        Parameters
        ----------
        `language`: :class:`VALID_LANGUAGES`
            The language of the riven items. Default: `"en"`.

        Returns
        -------
        :class:`list`[:class:`RivenItem`]

        Examples
        --------
        >>> async with PyTenno() as pytenno:
        >>>     riven_items = await pytenno.rivens.get_riven_items()
        >>>     for riven_item in riven_items:
        >>>         print(riven_item.url_name)
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

        Examples
        --------
        >>> async with PyTenno() as pytenno:
        >>>     riven_attributes = await pytenno.rivens.get_attributes()
        >>>     for riven_attribute in riven_attributes:
        >>>         print(riven_attribute.effect)
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

        Examples
        --------
        >>> async with PyTenno() as pytenno:
        >>>     locations = await pytenno.misc.get_locations()
        >>>     for location in locations:
        >>>         print(location.node_name)
        """
        return await self._get_locations(language)

    async def get_npcs(self, language: VALID_LANGUAGES = "en") -> list[DroptableNPC]:
        """Gets a list of all NPCs.

        Parameters
        ----------
        `language`: :class:`VALID_LANGUAGES`
            The language of the NPCs. Default: `"en"`.

        Returns
        -------
        :class:`list`[:class:`NPC`]

        Examples
        --------
        >>> async with PyTenno() as pytenno:
        >>>     npcs = await pytenno.misc.get_npcs()
        >>>     for npc in npcs:
        >>>         print(npc.name)
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
        :class:`list`[:class:`PartialMission`]

        Examples
        --------
        >>> async with PyTenno() as pytenno:
        >>>     missions = await pytenno.misc.get_missions()
        >>>     for mission in missions:
        >>>         print(mission.name)
        """
        return await self._get_missions(language)