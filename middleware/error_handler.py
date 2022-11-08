import logging

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from starlette import status

app = FastAPI()
#https://philstories.medium.com/fastapi-logging-f6237b84ea64
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)


async def hash_password_mismatch_exception_handler(request: Request, exc: HTTPException):
    logger = logging.getLogger(__name__)
    body = await request.body()
    logger.info(body)
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": f"Oops! unauthorized"},
    )


