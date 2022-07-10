from .._backends.misc import MiscBackend
from ..constants import VALID_LANGUAGES
from ..models.locations import Location
from ..models.missions import DroptableNPC, PartialMission


class Misc(MiscBackend):
    async def get_locations(self, language: VALID_LANGUAGES = "en") -> list[Location]:
        """Gets a list of all locations.

        Parameters
        ----------
        language : VALID_LANGUAGES
            The language of the locations. Default: ```"en"```.

        Returns
        -------
        list[Location]

        Example
        -------
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
        language : VALID_LANGUAGES
            The language of the NPCs. Default: ```"en"```.

        Returns
        -------
        list[NPC]

        Example
        -------
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
        language : VALID_LANGUAGES
            The language of the missions. Default: ```"en"```.

        Returns
        -------
        list[PartialMission]

        Example
        -------
        >>> async with PyTenno() as pytenno:
        >>>     missions = await pytenno.misc.get_missions()
        >>>     for mission in missions:
        >>>         print(mission.name)
        """
        return await self._get_missions(language)
