from typing import Optional

from .._backends.auth import AuthBackend
from ..constants import VALID_LANGUAGES
from ..models.users import CurrentUser


class Auth(AuthBackend):
    async def login(
        self,
        *,
        email: str,
        password: str,
        device_id: Optional[str] = None,
    ) -> CurrentUser:
        """Logs in the user with the given credentials.

        Parameters
        ----------
        email : str
            The email of the user.
        password : str
            The password of the user.
        device_id : str, optional
            The device ID of the user. This can be used to recognize the device between sessions. Default: None.

        Returns
        -------
        CurrentUser

        Example
        -------
        >>> async with PyTenno() as tenno:
        >>>     current_user = await tenno.auth.login(
        >>>         email="example@nothing.co"
        >>>         password="password"
        >>>     )
        >>>     print(current_user.ingame_name)
        """
        return await self._login(email, password, device_id)

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
        email : str
            The email of the user.
        password : str
            The password of the user.
        region : VALID_LANGUAGES
            The region of the user. Default: ``"en"``.
        device_id : str
            The device ID of the user, used to identify devices between sessions. Default: None.
        recaptcha : str
            The Google recaptcha response of the user. Default: None.

        Returns
        -------
        CurrentUser

        Example
        -------
        >>> async with PyTenno() as pytenno:
        >>>     email = "example@nothing.co"
        >>>     password = "password"
        >>>     region = "en"
        >>>     current_user = await pytenno.auth.register(email, password, region)
        >>>     print(current_user.ingame_name)

        """
        return await self._register(email, password, region, device_id, recaptcha)

    async def restore(self, email: str) -> None:
        """ "Sends the user a recovery email.

        Parameters
        ----------
        email: str
            The email of the user.

        Returns
        -------
        None

        Example
        -------
        >>> async with PyTenno() as pytenno:
        >>>     email = "example@nothing.co"
        >>>     await pytenno.auth.recover(email=email)
        """
        return await self._restore(email)