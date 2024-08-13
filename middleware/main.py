from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware as Trusted
from sentry_sdk import init
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from starlette.middleware.base import BaseHTTPMiddleware

from configs import configs
from library.logger import log_middleware


def add_middlewares(app: FastAPI) -> None:
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(Trusted, allowed_hosts=["localhost", "127.0.0.1", "0.0.0.0"])
    app.add_middleware(BaseHTTPMiddleware, dispatch=log_middleware)

    if configs.ENVIRONMENT != "test":
        app.state.limiter = Limiter(
            key_func=get_remote_address, default_limits=["5/minute"]
        )
        app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
        app.add_middleware(SlowAPIMiddleware)

        init(
            dsn=configs.SENTRY_DSN,
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
        )
        app.add_middleware(SentryAsgiMiddleware)
