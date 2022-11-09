import logging

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from starlette import status

app = FastAPI()

#https://philstories.medium.com/fastapi-logging-f6237b84ea64


async def unauthorized_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": f"Username or Password is incorrect"},
    )


