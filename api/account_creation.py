from fastapi import APIRouter, Depends
from sqlmodel import Session
from starlette import status
from starlette.responses import JSONResponse

from db.dbconfig import get_session
from crud.users_repository import UserRepository
from exceptions.CannotCreateUserError import CannotCreateUserError
from schemas.StaffUserCreateRequest import StaffUserCreateRequest

from utils.password_policy import policy

router = APIRouter()

"""
An endpoint which adds users to the database without any roles. This endpoint just creates an staff which does not have any rights.
"""
@router.post("/addUser")
async def create_staff_user(staff: StaffUserCreateRequest, session: Session = Depends(get_session), ur: UserRepository = Depends(UserRepository)):
    # The strength of the password in accordance to the set policy is tested
    strength = policy.password(staff.password).test()
    if strength:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={
            "message": "The password is not strong enough use at least 16 character, 2 Uppercase, 2 numbers, 2 specials, and 2 digits"})
    # create a staff if it does not exist
    try:
        data = ur.create_user_or_else_return_none(session, staff)
        # if staff already exists then return forbidden
        if data is None:
            # The error Cannot create staff does not give information why the creation failed, providing less information for others to abuse
            return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"message": "Cannot create staff"})
        return JSONResponse(status_code=status.HTTP_201_CREATED, content={})
    except CannotCreateUserError as e:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": f"{e.message}"})
