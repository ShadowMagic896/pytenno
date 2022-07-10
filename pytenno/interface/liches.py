from .._backends.liches import LichesBackend
from ..constants import VALID_LANGUAGES
from ..models.liches import LichEphemera, LichQuirk, LichWeapon


class Liches(LichesBackend):
    async def get_weapons(self, language: VALID_LANGUAGES = "en") -> list[LichWeapon]:
        """Gets all weapons.

        Parameters
        ----------
        language : VALID_LANGUAGES
            The language of the weapons. Default: ``"en"``.

        Returns
        -------
        list[LichWeapon]

        Example
        -------
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
        language : VALID_LANGUAGES
            The language of the ephemeras. Default: ``"en"``.

        Returns
        -------
        list[LichEphemera]

        Example
        -------
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
        language : VALID_LANGUAGES
            The language of the quirks. Default: ```"en"```.

        Returns
        -------
        list[LichQuirk]

        Example
        -------
        >>> async with PyTenno() as pytenno:
        >>>     quirks = await pytenno.liches.get_quirks()
        >>>     for quirk in quirks:
        >>>         print(quirk.url_name)
        """
        return await self._get_quirks(language)
