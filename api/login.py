from datetime import datetime

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHash, VerificationError
from fastapi import APIRouter, Depends
from sqlmodel import Session
from starlette import status
from starlette.responses import JSONResponse

from config.models.ApplicationSettings import ApplicationSettings
from db.dbconfig import get_session
from db.models import Staff
from crud.users_repository import UserRepository
from exceptions.UserNotFoundError import UserNotFoundError
from schemas.StaffLoginRequest import StaffLoginRequest
from schemas.TokenResponse import TokenResponse
from utils.jwt_utils import encode_jwt
from utils.logging import get_logger

MINUTES_IN_AN_HOUR = 60

router = APIRouter()

"""
Endpoint which verify the password. 
"""
# Depends() is a function which is in fastAPI to do dependency injection. Using Dependency Injection it is easier to mock it in the automated tests.
@router.post("/authenticate", responses={401: {"message": f"Oops! unauthorized"}})
async def authenticate_staff(user: StaffLoginRequest, session: Session = Depends(get_session), ur: UserRepository = Depends(UserRepository)):
    # get the logger
    log = get_logger(__name__)
    ph = PasswordHasher()
    try:
        db_user: Staff = ur.get_user_id(session, user.username)
        # Checks if the login attempts is exceeded
        if is_login_count_exceeded(db_user):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN,
                content={"message": f"Staff is blocked due to too many attempts"},
            )
        # Verify the password using safe function verify. This is more resilient against side-channel attack, instead of string comparison
        ph.verify(db_user.password, user.password)
        ur.reset_login_counter_for_user(session, user.username)
    except (VerifyMismatchError, InvalidHash, VerificationError) as e:
        log.exception(e, exc_info=True)
        return handle_incorrect_password(session, ur, user)
    except UserNotFoundError as e:
        # A Http 401 is returned instead of HTTP 404 not found, so that the external entity does not get extra information that the username is not found.
        log.exception(e, exc_info=True)
        return handle_user_not_found()
    # An Oauth signed token is returned as the result of successful authentication
    token = TokenResponse(token=encode_jwt())
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=token.dict())


"""
Function which checks if the the max login count and the blocked time as well.
"""
def is_login_count_exceeded(db_user: Staff) -> bool:
    delta = (datetime.utcnow().timestamp() - db_user.modified_timestamp.timestamp()) / MINUTES_IN_AN_HOUR
    return db_user.login_counter >= ApplicationSettings.LOGIN_MAX_ATTEMPT_COUNT and delta <= ApplicationSettings.LOGIN_USER_BLOCKED_TIME_MINUTES


"""
Function that handles the http response when the staff is not found.
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
def handle_incorrect_password(session: Session, ur: UserRepository, user: StaffLoginRequest) -> JSONResponse:
    ur.increment_login_counter_for_user(session, user.username)
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"message": f"Username or Password is incorrect"},
    )
