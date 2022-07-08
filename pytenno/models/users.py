from construct import stream_iseof
from dataclasses import dataclass
from datetime import datetime
from pyrsistent import m
from pytenno.utils import from_data

from .enums import PatreonBadge, UserStatus


@dataclass
class PatreonProfile:
    patreon_founder: bool
    subscription: bool
    patreon_badge: PatreonBadge = None


@dataclass
class BaseUser:
    id: str
    ingame_name: str
    region: str

    # Path to user avatar in static folder.
    avatar: str | None = None

    def __repr__(self):
        return f"<User id={self.id} ingame_name={self.ingame_name}>"


@dataclass
class LinkedProfiles:
    discord_profile: bool
    patreon_profile: bool
    xbox_profile: bool
    steam_profile: bool


@dataclass(kw_only=True)
class CurrentUser(BaseUser):
    anonymous: bool
    verification: bool
    check_code: str
    role: str
    platform: str
    banned: bool
    ban_reason: str | None = None
    background: str | None = None
    has_mail: bool
    reputation: int
    linked_accounts: LinkedProfiles

    patreon_profile: PatreonProfile
    # how many reviews user wrote today
    written_reviews: int
    unread_messages: int

    def _from_data(node: dict):
        return CurrentUser(
            # file deepcode ignore WrongNumberOfArguments
            patreon_profile=from_data(PatreonProfile, node.pop("patreon_profile")),
            linked_accounts=LinkedProfiles(**node.pop("linked_accounts")),
            **node,
        )


@dataclass(kw_only=True)
class UserShort(BaseUser):
    status: UserStatus
    reputation: int
    last_seen: datetime | None
