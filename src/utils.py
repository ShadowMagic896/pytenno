from functools import cache
from urllib.parse import quote

from .constants import VALID_TRANSLATIONS_RAW
from .errors import BaseError


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
    raise error from None


def _create_languages(data: dict, lang_in_item: type, drop: type):
    return {
        lang.replace("-", "_"): lang_in_item(
            item_name=vals["item_name"],
            description=vals["description"],
            wiki_link=vals["wiki_link"],
            drop=[drop(name=node["name"], link=node["link"]) for node in vals["drop"]],
        )
        for lang, vals in data.items()
        if lang in VALID_TRANSLATIONS_RAW
    }
