import json

from fastapi import APIRouter
from starlette.responses import JSONResponse

from models.UserLoginRequest import UserLoginRequest

router = APIRouter()


@router.post("/authenticate")
async def authenticate_staff(user: UserLoginRequest):
    return JSONResponse(status_code=200,
                        content={"hello": "handshake"})
