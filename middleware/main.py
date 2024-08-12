from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware as Trusted
from sentry_sdk import init
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from configs import configs
from library.logger import log_middleware


def add_middlewares(app: FastAPI) -> None:
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(Trusted, allowed_hosts=["localhost", "127.0.0.1", "0.0.0.0"])
    app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)

    if configs.ENVIRONMENT != "test":
        init(
            dsn=configs.SENTRY_DSN,
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
        )
        app.add_middleware(SentryAsgiMiddleware)
