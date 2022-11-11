from fastapi import APIRouter, Depends
from sqlmodel import Session
from starlette import status
from starlette.responses import JSONResponse

from db.dbconfig import get_session
from crud.users_repository import UserRepository
from schemas.UserCreateRequest import UserCreateRequest

from utils.password_policy import policy

router = APIRouter()

"""
An endpoint which adds users to the database without any roles. This endpoint just creates an user which does not have any rights.
"""
@router.post("/addUser")
async def create_staff_user(*, session: Session = Depends(get_session), user: UserCreateRequest):
    # The strength of the password in accordance to the set policy is tested
    strength = policy.password(user.password).test()
    if strength:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
            "message": "The password is not strong enough use at least 16 character, 2 Uppercase, 2 numbers, 2 specials, and 2 digits"})
    ur = UserRepository()
    # create a user if it does not exist
    data = ur.create_user_or_else_return_none(session, user)
    # if user already exists then return forbidden
    if data is None:
        # The error Cannot create user does not give information why the creation failed, providing less information for others to abuse
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"message": "Cannot create user"})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={})
