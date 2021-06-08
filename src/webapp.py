import logging
import os

from fastapi import FastAPI

from src.config import AppConfig
from src.endpoints.limit import router as decision_router

log = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s %(message)s", level=AppConfig.LOG_LEVEL)


def create_app() -> FastAPI:
    url_prefix = os.environ.get("URL_PREFIX", "/").rstrip("/")

    app = FastAPI(
        title="Viaduct", version=AppConfig.APP_VERSION, openapi_prefix=url_prefix
    )

    app.include_router(decision_router)

    # No URL prefix: return app as-is
    if url_prefix == "":
        return app

    # URL prefix: mount the app inside of another app
    root = FastAPI()
    root.mount(url_prefix, app)
    return root
