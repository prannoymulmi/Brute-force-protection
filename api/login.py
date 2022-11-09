from argon2.exceptions import VerifyMismatchError, InvalidHash, VerificationError
from fastapi import APIRouter, Depends
from sqlmodel import Session
from starlette import status
from starlette.responses import JSONResponse
from argon2 import PasswordHasher

from db.dbconfig import get_session
from db.models import User
from db.users_repository import UserRepository
from exceptions.UserNotFoundError import UserNotFoundError
from models.UserLoginRequest import UserLoginRequest

router = APIRouter()

"""
Endpoint which verify the password 
"""


@router.post("/authenticate", responses={401: {"message": f"Oops! unauthorized"}})
async def authenticate_staff(*, session: Session = Depends(get_session), user: UserLoginRequest):
    ph = PasswordHasher()
    ur = UserRepository()
    try:
        # ur.create_user(user.username, user.password)
        db_user: User = ur.get_user_id(session, user.username)
        ph.verify(db_user.password, user.password)
    except (VerifyMismatchError, InvalidHash, VerificationError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": f"Oops! unauthorized"},
        )
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={'token': 'hello'})
