from dataclasses import dataclass


@dataclass
class LinkedAccounts:
    steam_profile: bool
    patreon_profile: bool
    xbox_profile: bool
    switch_profile: bool
