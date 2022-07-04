import datetime
from dataclasses import dataclass
from functools import cached_property


class ObjectID(str):
    pass


@dataclass
class DateTime:
    original: str

    @cached_property
    def dt(self) -> datetime.datetime:
        return datetime.datetime.strptime(self.original, "%Y-%m-%dT%H:%M:%S.%f%z")

    def __repr__(self) -> str:
        return f"<DateTime at {self.original}>"
