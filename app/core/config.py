import logging
from typing import List

from loguru import logger
import sys
from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings, Secret
from app.core.logging import InterceptHandler

config = Config(".env")

# ******application settigs******
DEBUG: bool = config("DEBUG", cast=bool, default=False)
SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret, default="secret")
API_PREFIX: str = config("API_PREFIX", default="api")
PROJECT_NAME: str = config("PROJECT_NAME", default="GeoHack Api")
ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS",
    cast=CommaSeparatedStrings,
    default="*",
)


# *****database settings*****
DATABASE_URL: str = config("DB_CONNECTION", default="")
DB_USER: str = config("DB_USER", default="geohack")
DB_NAME: str = config("DB_NAME", default="geohack-db")
DB_PASS: str = config("DB_PASS", default="password")
DB_HOST: str = config("DB_HOST", default="localhost")
MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)


# *****Externals*****
# *****LINE*****
LINE_CHANNEL_ACCESS_TOKEN: str = config("LINE_CHANNEL_ACCESS_TOKEN", default="")
LINE_CHANNEL_SECRET: str = config("LINE_CHANNEL_SECRET", default="")

# *****GoogleCloudPlatform*****
GCP_STORAGE_BUCKET_NAME: str = config(
    "GCP_STORAGE_BUCKET_NAME", default="geohack-static"
)


# *****Logging*****
LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO
LOGGERS = ("uvicorn.asgi", "uvicorn.access")
logging.getLogger().handlers = [InterceptHandler()]
for logger_name in LOGGERS:
    logging_logger = logging.getLogger(logger_name)
    logging_logger.handlers = [InterceptHandler(level=LOGGING_LEVEL)]

logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
