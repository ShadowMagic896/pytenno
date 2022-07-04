from dataclasses import dataclass

from .enums import PatreonBadge, UserStatus
from .formats import DateTime, ObjectID


@dataclass
class PatreonProfile:
    patreon_founder: bool
    subscription: bool
    patreon_badge: PatreonBadge


@dataclass
class BaseUser:
    id: ObjectID
    ingame_name: str
    region: str

    # Path to user avatar in static folder.
    avatar: str | None


@dataclass
class CurrentUser(BaseUser):
    anonymous: bool
    verification: bool
    check_code: str
    role: str
    patreon_profile: PatreonProfile
    platform: str
    banned: bool
    ban_reason: str
    background: str
    has_email: bool

    # how many reviews user wrote today
    written_reviews: int
    unread_messages: int


@dataclass
class UserShort(BaseUser):
    status: UserStatus
    reputation: int
    last_seen: DateTime | None
