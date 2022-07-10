from .._backends.rivens import RivensBackend
from ..constants import VALID_LANGUAGES
from ..models.rivens import RivenAttribute, RivenItem


class Rivens(RivensBackend):
    async def get_riven_items(
        self, language: VALID_LANGUAGES = "en"
    ) -> list[RivenItem]:
        """Gets a list of all riven-equippable items.

        Parameters
        ----------
        language : VALID_LANGUAGES
            The language of the riven items. Default: ```"en"```.

        Returns
        -------
        list[RivenItem]

        Example
        -------
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
        language : VALID_LANGUAGES
            The language of the riven attributes. Default: ```"en"```.

        Returns
        -------
        list[RivenAttribute]

        Example
        -------
        >>> async with PyTenno() as pytenno:
        >>>     riven_attributes = await pytenno.rivens.get_attributes()
        >>>     for riven_attribute in riven_attributes:
        >>>         print(riven_attribute.effect)
        """
        return await self._get_riven_attributes(language)
