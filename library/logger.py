from logging import getLogger, Formatter, StreamHandler, FileHandler, INFO
from fastapi import Request
from sys import stdout
from time import time

logger = getLogger()

formatter = Formatter(
    fmt="%(asctime)s - %(levelname)s - %(levelno)s - %(pathname)s - %(message)s"
)

stream_handler = StreamHandler(stdout)
file_handler = FileHandler("app.log")

stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.handlers = [stream_handler, file_handler]


logger.setLevel(INFO)


async def log_middleware(request: Request, call_next):
    start = time()
    response = await call_next(request)
    process_time = time() - start

    log_dict = {
        "url": request.url.path,
        "method": request.method,
        "process_time": process_time,
    }
    logger.info(log_dict, extra=log_dict)

    return response
