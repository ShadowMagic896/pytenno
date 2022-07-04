from enum import Enum


class Base(Enum):
    def __int__(self):
        return self.value

    def __str__(self):
        return self.name.capitalize()


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


class ItemRarity(Base):
    very_command = 0
    common = 1
    uncommon = 2
    rare = 3
    legendary = 4
    peculiar = 5


class OrderType(Base):
    buy = 0
    sell = 1


class Element(Base):
    impact = 0
    heat = 1
    cold = 2
    electricity = 3
    toxin = 4
    magnetic = 5
    radiation = 6


class UserPatreonBadge(Base):
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


class RivenGroup(Base):
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


class Polarity(Base):
    madurai = 0
    vazarin = 1
    naramon = 2
    zanurik = 3


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


class AuctionType:
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
    _1: 0
    _2: 1
    _3: 2
    _4: 3
    final: 4
