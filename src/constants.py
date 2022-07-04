from typing import Final, Literal


MAIN_ROOT: Final[str] = "https://warframe.market"
API_ROOT: Final[str] = "https://api.warframe.market/v1"
ASSET_ROOT: Final[str] = "https://warframe.market/static/assets"

VALID_TRANSLATIONS = Literal[
    "en",
    "ru",
    "ko",
    "fr",
    "sv",
    "de",
    "zh-hant",
    "zh_hant",
    "zh-hans",
    "zh_hant",
    "pt",
    "es",
    "pl",
]

VALID_TRANSLATIONS_RAW = {
    "en",
    "ru",
    "ko",
    "fr",
    "sv",
    "de",
    "zh-hant",
    "zh_hant",
    "zh-hans",
    "zh_hant",
    "pt",
    "es",
    "pl",
}
