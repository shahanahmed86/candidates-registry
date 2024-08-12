from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware as Trusted
from sentry_sdk import init
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from slowapi.middleware import SlowAPIMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler, Limiter
from slowapi.util import get_remote_address

from configs import configs
from library.logger import log_middleware

def add_middlewares(app: FastAPI) -> None:
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    app.add_middleware(Trusted, allowed_hosts=["localhost", "127.0.0.1", "0.0.0.0"])
    app.add_middlewarue(BaseHTTPMiddleware, dispatch=log_middleware)

    app.state.limiter = Limiter(key_func=get_remote_address, default_limits=["5/minute"])
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_middleware(SlowAPIMiddleware)

    if configs.ENVIRONMENT != "test":
        init(
            dsn=configs.SENTRY_DSN,
            traces_sample_rate=1.0,
            profiles_sample_rate=1.0,
        )
        app.add_middleware(SentryAsgiMiddleware)
