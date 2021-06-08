import logging

from starlette.config import Config

config = Config(".env")


class AppConfig:
    DEBUG: bool = config("DEBUG", cast=bool, default=False)
    APP_VERSION: str = config("APPVERSION", cast=str, default="latest")

    LOG_LEVEL: str = logging.getLevelName(
        config("LOGLEVEL", cast=str, default=logging.WARNING)
    )
