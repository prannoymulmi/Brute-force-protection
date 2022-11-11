from datetime import datetime

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash, VerificationError
from fastapi import APIRouter, Depends
from sqlmodel import Session
from starlette import status
from starlette.responses import JSONResponse

from config.models.ApplicationSettings import ApplicationSettings
from db.dbconfig import get_session
from db.models import User
from crud.users_repository import UserRepository
from exceptions.UserNotFoundError import UserNotFoundError
from schemas.UserLoginRequest import UserLoginRequest

router = APIRouter()

"""
Endpoint which verify the password 
"""
@router.post("/authenticate", responses={401: {"message": f"Oops! unauthorized"}})
async def authenticate_staff(*, session: Session = Depends(get_session), user: UserLoginRequest):
    ph = PasswordHasher()
    ur = UserRepository()
    try:
        db_user: User = ur.get_user_id(session, user.username)
        # Checks if the login attempts is exceeded
        if is_login_count_exceeded(db_user):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"message": f"User is blocked due to too many attempts"},
            )
        ph.verify(db_user.password, user.password)
        ur.reset_login_counter_for_user(session, user.username)
    except (VerifyMismatchError, InvalidHash, VerificationError):
        return handle_incorrect_password(session, ur, user)
    except UserNotFoundError:
        return handle_user_not_found()
    # Using fake token but an Oauth flow using access and refresh token is a suitable implementation
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={'token': 'some_token'})


"""
Function which checks if the the max login count and the blocked time as well.
"""
def is_login_count_exceeded(db_user: User) -> bool:
    delta = (datetime.utcnow().timestamp() - db_user.modified_timestamp.timestamp()) / 60
    return db_user.login_counter >= ApplicationSettings.LOGIN_MAX_ATTEMPT_COUNT and delta <= ApplicationSettings.LOGIN_USER_BLOCKED_TIME_MINUTES


"""
Function that handles the http response when the user is not found.
"""
def handle_user_not_found() -> JSONResponse:
    # A Http 401 is returned instead of HTTP 404 not found, so that the external entity does not get extra information that the username is not found.
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": f"Username or Password is incorrect"},
    )


"""
Function which handles the http response when the password verification fails.
"""
def handle_incorrect_password(session: Session, ur: UserRepository, user: UserLoginRequest) -> JSONResponse:
    ur.increment_login_counter_for_user(session, user.username)
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": f"Username or Password is incorrect"},
    )
