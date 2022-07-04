from dataclasses import dataclass
from pyrsistent import m

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

    def __repr__(self):
        return f"<User id={self.id} ingame_name={self.ingame_name}>"


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

    def _from_data(node: dict):
        return UserShort(
            id=ObjectID(node["id"]),
            ingame_name=node["ingame_name"],
            region=node["region"],
            avatar=node["avatar"],
            status=UserStatus[node["status"]],
            reputation=node["reputation"],
            last_seen=DateTime(last_seen)
            if (last_seen := node["last_seen"]) is not None
            else None,
        )
