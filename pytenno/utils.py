import datetime
from enum import Enum
from functools import cache
from pytenno.models.liches import LichQuirk
from pytenno.models.rivens import PartialRivenAttribute
from typing import Any, Callable, Mapping, Type
from urllib.parse import quote

from .constants import ASSET_ROOT, VALID_TRANSLATIONS_RAW
from .errors import BaseError
from .models.droptable import Drop
from .models.enums import (
    AnimationFormat,
    AuctionMarking,
    AuctionType,
    Element,
    Faction,
    IconFormat,
    ItemRarity,
    MeasurementUnit,
    OrderType,
    PatreonBadge,
    Platform,
    Polarity,
    RivenAttributeGroup,
    RivenWeaponGroup,
    RivenWeaponType,
    Rotation,
    Stage,
    Subtype,
    UserRole,
    UserStatus,
)
from .models.items import LangInItem


@cache
def format_name(name: str):

    return quote(name.lower().replace(" ", "_"))


@cache
def _raise_error_code(code: int):

    for error in BaseError.__subclasses__():

        if error.code == code:
            raise error

    error = BaseError

    error.code = code

    error.msg = "Unknown error occurred"

    raise error


DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S.%f%z"


# Enums that take in a value and return an enum value
_ENUM_MAPPING: Mapping[str, Type[Enum]] = {
    "rarity": ItemRarity,
    "order_type": OrderType,
    "element": Element,
    "patreon_badge": PatreonBadge,
    "platform": Platform,
    "role": UserRole,
    "status": UserStatus,
    "polarity": Polarity,
    "riven_type": RivenWeaponType,
    "icon_format": IconFormat,
    "animation_format": AnimationFormat,
    "rotation": Rotation,
    "type": AuctionType,
    "is_marked_for": AuctionMarking,
    "faction": Faction,
}

# Enums that require special attention
_SPECIAL_ENUM_MAPPING: Mapping[str, Callable[[str], Type[Enum]]] = {
    "subtypes": lambda names: [Subtype[name] for name in names],
    "attributes": lambda attributes: [
        PartialRivenAttribute[name] for name in attributes
    ],
    "exclusive_to": lambda excls: [RivenWeaponGroup[exc] for exc in excls],
    "units": lambda unit: MeasurementUnit[unit],
    "group": lambda grp: RivenAttributeGroup[
        grp
    ]  # The API is ambigous on this attribute; three different items have the name but can have different values
    if hasattr(RivenAttributeGroup, grp)
    else RivenWeaponGroup[grp]
    if hasattr(RivenWeaponGroup, grp)
    else grp,
    "stage": lambda stage: Stage[f"_{stage}" if stage.isdigit() else stage],
    "is_marked_for": lambda mark: AuctionMarking[mark] if mark is not None else None,
}


def _from_data(cls_: type, data: dict[str, Any]):
    print(cls_)
    nd = {}  # Create new dict to avoid RuntimeErrors
    for key, value in data.items():
        if value is None:
            continue
        if key in ("icon", "sub_icon", "thumb", "avatar"):
            nd[key] = f"{ASSET_ROOT}/{value}"
        elif key in (
            "creation_date",
            "created",
            "last_updated",
            "updated",
            "last_seen",
            "marked_operation_at",
        ):
            nd[key] = datetime.datetime.strptime(value, DATETIME_FORMAT)
        elif key in VALID_TRANSLATIONS_RAW:
            nd[key.replace("-", "_")] = LangInItem(**value)
        elif key == "drop":
            nd[key] = [Drop(**val) for val in value]
        else:
            try:
                nd[key] = _ENUM_MAPPING[key][value]
            except KeyError:
                try:
                    nd[key] = _SPECIAL_ENUM_MAPPING[key](value)
                except KeyError:
                    nd[key] = value

    if hasattr(cls_, "_from_data"):
        return cls_._from_data(nd)
    return cls_(**nd)
