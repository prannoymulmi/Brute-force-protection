
from argon2.exceptions import VerifyMismatchError, InvalidHash, VerificationError
from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse
from argon2 import PasswordHasher

from db.users_repository import UserRepository
from models.UserLoginRequest import UserLoginRequest

router = APIRouter()


@router.post("/authenticate", responses={401: {"message": f"Oops! unauthorized"}})
async def authenticate_staff(user: UserLoginRequest):
    ph = PasswordHasher()
    hashed_password = ph.hash("test")
    ur = UserRepository()
    ur.create_user(user.username, ph.hash(user.password))
    try:
        ph.verify(hashed_password, user.password)
    except (VerifyMismatchError, InvalidHash, VerificationError):

        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"message": f"Oops! unauthorized"},
        )
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={'token': 'hello'})
