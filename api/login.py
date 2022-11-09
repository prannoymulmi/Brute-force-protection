
from argon2.exceptions import VerifyMismatchError, InvalidHash, VerificationError
from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse
from argon2 import PasswordHasher

from db.models import User
from db.users_repository import UserRepository
from exceptions.UserNotFoundError import UserNotFoundError
from models.UserLoginRequest import UserLoginRequest

router = APIRouter()


@router.post("/authenticate", responses={401: {"message": f"Oops! unauthorized"}})
async def authenticate_staff(user: UserLoginRequest):
    ph = PasswordHasher()
    ur = UserRepository()
    try:
        db_user: User = ur.get_user_id(user.username)
        ph.verify(db_user.password, user.password)
    except (VerifyMismatchError, InvalidHash, VerificationError, UserNotFoundError):

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": f"Oops! unauthorized"},
        )
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={'token': 'hello'})
