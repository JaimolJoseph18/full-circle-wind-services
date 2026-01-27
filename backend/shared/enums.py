from enum import Enum, IntEnum


class ApiStatusCode(IntEnum):
    OK = 200
    CREATED = 201
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_ERROR = 500

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            try:
                return cls(int(value))
            except ValueError:
                pass
        return None
    

class EmailStatus(Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
    BOUNCED = "bounced"
    BLOCKED = "blocked"


class ApiStatusMessages(Enum):
    DATA_RECEIVED = "Data Received"
    ERROR = "error"
    TIMEOUT = "timeout"
    UNAUTHORIZED = "unauthorized"
    NOT_FOUND = "not_found"
    SERVER_ERROR = "server_error"
    FORBIDDEN = "forbidden"