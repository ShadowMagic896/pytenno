from dataclasses import dataclass


@dataclass
class BaseError(BaseException):
    code: int
    msg: str

    def __init__(self, *args: object) -> None:
        super().__init__(f"Error [Code {self.code}]: {self.msg}")


class Missing(BaseError):
    code = 404
    msg = "Cannot find requested object"
