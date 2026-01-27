from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings
from pathlib import Path


p: Path = Path(__file__).parents[2] / ".env"

config: Config = Config(p if p.exists() else None)

ALLOWED_HOSTS: CommaSeparatedStrings = config(
    "ALLOWED_HOSTS", cast=CommaSeparatedStrings, default="localhost"
)

API_KEY:  str = config("API_KEY", cast=str)
ENDPOINT: str = config("ENDPOINT", cast=str)
MAIL_USERNAME: str = config("MAIL_USERNAME", cast=str)
MAIL_PASSWORD: str = config("MAIL_PASSWORD", cast=str)
MAIL_PORT: str = config("MAIL_PORT", cast=str, default=578)
MAIL_SERVER: str = config("MAIL_SERVER", cast=str, default="smtp.gmail.com")
MAIL_FROM: str = config("MAIL_FROM", cast=str)
MAIL_TO: str = config("MAIL_TO", cast=str)
