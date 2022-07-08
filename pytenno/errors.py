from dataclasses import dataclass


@dataclass
class BaseError(BaseException):
    code: int
    msg: str

    def __init__(self, *args: object) -> None:
        super().__init__(f"Error [Code {self.code}]: {self.msg}")


class Missing(BaseError):
    code = 404
    msg = "Undocumented"


class BadRequest(BaseError):
    code = 400
    msg = "Invalid request"


class Unauthorized(BaseError):
    code = 401
    msg = "Unauthorized"


class InternalServerError(BaseError):
    code = 500
    msg = "Internal server error"
