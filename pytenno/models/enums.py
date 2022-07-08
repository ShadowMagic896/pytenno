from enum import Enum
from typing_extensions import Self


class Base(Enum):
    def __int__(self):
        return self.value

    def __str__(self):
        return self.name


class RelicQuality(Base):
    intact = 0
    exceptional = 1
    flawless = 2
    radiant = 3


class FishSize(Base):
    small = 0
    medium = 1
    large = 2


class FortunaFishQuality(Base):
    basic = 0
    adorned = 1
    magnificent = 2


class Subtype(Base):
    intact = 0
    exceptional = 1
    flawless = 2
    radiant = 3
    small = 4
    medium = 5
    large = 5
    basic = 6
    adorned = 7
    magnificent = 8


class ItemRarity(Base):
    very_common = 0
    common = 1
    uncommon = 2
    rare = 3
    legendary = 4
    peculiar = 5


class OrderType(Base):
    buy = 0
    sell = 1


class MeasurementUnit(Base):
    seconds = 0
    percent = 1


class Element(Base):
    impact = 0
    heat = 1
    cold = 2
    electricity = 3
    toxin = 4
    magnetic = 5
    radiation = 6


class PatreonBadge(Base):
    bronze = 0
    silver = 1
    gold = 2
    platinum = 3


class Platform(Base):
    ps4 = 0
    pc = 1
    xbox = 2
    switch = 3


class UserRole(Base):
    anonymous = 0
    user = 1
    moderator = 2
    admin = 3


class UserStatus(Base):
    offline = 0
    online = 1
    ingame = 2


class RivenWeaponGroup(Base):
    primary = 0
    secondary = 1
    melee = 2
    zaw = 3
    sentinel = 4
    archgun = 5
    kitgun = 6


class RivenAttributeGroup(Base):
    default = 0
    melee = 1
    top = 2


class RivenWeaponType(Base):
    rifle = 0
    shotgun = 1
    pistol = 2
    melee = 3
    zaw = 4
    kitgun = 5


class Polarity(Base):
    madurai = 0
    vazarin = 1
    naramon = 2
    zanurik = 3
    any = 4


class RivenType(Base):
    shotgun = 0
    rifle = 1
    pistol = 2
    melee = 3
    zaw = 4
    kitgun = 5


class TranslationLanguage(Base):
    en = 0
    ru = 1
    ko = 2
    fr = 3
    sv = 4
    de = 5
    zh_hant = 6
    zh_hans = 7
    pt = 8
    es = 9
    pl = 10


class IconFormat(Base):
    land = 0
    port = 1


AnimationFormat = IconFormat


class AuctionType(Base):
    riven = 0
    lich = 1
    kubrow = 2


class AuctionMarking(Base):
    removing = 0
    archiving = 1


class Rotation(Base):
    a = 0
    b = 1
    c = 2


class Stage(Base):
    _1 = 0
    _2 = 1
    _3 = 2
    _4 = 3
    final = 4


class Faction(Base):
    infested = 0
    grineer = 1
    corpus = 2
    corrupted = 3


class RivenStat(Base):
    ammo_maximum = 0
    cold = 1
    critical_chance = 2
    damage = 3
    damage_vs_corpus = 4
    damage_vs_grineer = 5
    damage_vs_infested = 6
    electricity = 7
    fire_rate_attack_speed = 8
    heat = 9
    impact = 10
    magazine_capacity = 11
    multishot = 12
    projectile_speed = 13
    punch_through = 14
    puncture = 15
    reload_speed = 16
    slash = 17
    status_chance = 18
    status_duration = 19
    toxin = 20
    weapon_recoil = 21
    initial_combo = 22
    range = 23
    chance_to_gain_extra_combo_count = 24
    combo_duration = 25
    critical_chance_on_slide_attack = 26
    finisher_damage = 27
    channeling_efficiency = 28
    channeling_damage = 29

    def __str__(self):
        # Some of these values have non-python-friendly names
        if self.value == 3:
            return "base_damage_/_melee_damage"
        elif self.value == 8:
            return "fire_rate_/_attack_speed"
        return self.name
