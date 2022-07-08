from dataclasses import dataclass


@dataclass
class BaseError(BaseException):
    code: int
    msg: str

    def __init__(self, *args: object) -> None:
        super().__init__(f"Error [Code {self.code}]: {self.msg}")

# Create an eror class for every error response and code I can recieve
# It should properly be inherited from BaseError

class BadRequest(BaseError):
    code = 400
    msg = "Bad Request"


class Unauthorized(BaseError):
    code = 401
    msg = "Unauthorized"


class Forbidden(BaseError):
    code = 403
    msg = "Forbidden"


class NotFound(BaseError):
    code = 404
    msg = "Not Found"


class Conflict(BaseError):
    code = 409
    msg = "Conflict"


class InternalServerError(BaseError):
    code = 500
    msg = "Internal Server Error"


class NotImplemented(BaseError):
    code = 501
    msg = "Not Implemented"


class BadGateway(BaseError):
    code = 502
    msg = "Bad Gateway"


class ServiceUnavailable(BaseError):
    code = 503
    msg = "Service Unavailable"


class GatewayTimeout(BaseError):
    code = 504
    msg = "Gateway Timeout"