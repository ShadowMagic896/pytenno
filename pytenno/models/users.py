from dataclasses import dataclass
from datetime import datetime

from ..utils import from_data
from .enums import PatreonBadge, Platform, UserRole, UserStatus


@dataclass
class PatreonProfile:

    """Represents a Patreon profile.

    Parameters
    ----------
    patreon_founder : bool
        Whether the user is a Patreon founder.

    subscription : bool
        Whether the user is a Patreon subscriber.

    patreon_badge : PatreonBadge , optional
        The Patreon badge of the user.
    """

    patreon_founder: bool
    subscription: bool
    patreon_badge: PatreonBadge | None = None


@dataclass
class BaseUser:

    """Base class that other user classes inherit from.

    Parameters
    ----------
    id : str
        The ID of the user.

    ingame_name : str
        The ingame name of the user.

    region : str
        The region the user is on.

    avatar : str , optional
        The URL of the user's avatar.
    """

    id: str
    ingame_name: str
    region: str
    avatar: str | None = None

    def __repr__(self):
        return f"<User id={self.id} ingame_name={self.ingame_name}>"


@dataclass
class LinkedProfiles:
    """Represents a user's linked profiles.

    Parameters
    ----------
    discord_profile : bool
        Whether the user has a Discord profile linked to their warframe.market profile.

    patreon_profile : bool
        Whether the user has a Patreon profile linked to their warframe.market profile.

    xbox_profile : bool
        Whether the user has a Xbox profile linked to their warframe.market profile.

    steam_profile : bool
        Whether the user has a Steam profile linked to their warframe.market profile.
    """

    discord_profile: bool
    patreon_profile: bool
    xbox_profile: bool
    steam_profile: bool


@dataclass(kw_only=True)
class CurrentUser(BaseUser):
    """Represents the current user. This is the user that is logged in.

    Parameters
    ----------
    id : str
        The ID of the user.

    ingame_name : str
        The ingame name of the user.

    region : str
        The region the user is on.

    avatar : str , optional
        The URL of the user's avatar.

    anonymous : bool
        Whether the user is anonymous.

    verification : bool
        Whether the user is verified.

    check_code : str
        The check code of the user.

    role : UserRole
        The role of the user.

    platform : Platform
        The platform of the user.

    banned : bool
        Whether the user is banned.

    ban_reason : str , optional
        The reason the user is banned. If None, the user is not banned.

    background : str , optional
        The URL of the user's background. If None, the user has no background.

    has_mail : bool
        Whether the user has unread mail.

    reputation : int
        The reputation of the user.

    linked_accounts : LinkedProfiles
        The linked accounts of the user.

    patreon_profile : PatreonProfile
        The Patreon profile of the user.

    written_reviews : int
        The number of reviews the user has written today.

    unread_messages : int
        The number of unread messages the user has.
    """

    anonymous: bool
    verification: bool
    check_code: str
    role: UserRole
    platform: Platform
    banned: bool
    ban_reason: str | None = None
    background: str | None = None
    has_mail: bool
    reputation: int
    linked_accounts: LinkedProfiles
    patreon_profile: PatreonProfile
    written_reviews: int
    unread_messages: int

    def from_data(node: dict):
        return CurrentUser(
            # file deepcode ignore WrongNumberOfArguments
            patreon_profile=from_data(PatreonProfile, node.pop("patreon_profile")),
            linked_accounts=LinkedProfiles(**node.pop("linked_accounts")),
            **node,
        )


@dataclass(kw_only=True)
class UserShort(BaseUser):
    """Represents a user.

    Parameters
    ----------
    id : str
        The ID of the user.

    ingame_name : str
        The ingame name of the user.

    region : str
        The region the user is on.

    avatar : str , optional
        The URL of the user's avatar.

    status : UserStatus
        The status of the user.

    reputation : int
        The reputation of the user.

    last_seen : datetime.datetime , optional
        The last time the user was seen. If None, the user has not been seen.
    """

    status: UserStatus
    reputation: int
    last_seen: datetime | None
