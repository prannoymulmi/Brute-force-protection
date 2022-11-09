from fastapi import APIRouter, Depends
from sqlmodel import Session
from starlette import status
from starlette.responses import JSONResponse

from db.dbconfig import get_session
from db.users_repository import UserRepository
from models.UserCreateRequest import UserCreateRequest

router = APIRouter()


@router.post("/addUser")
async def create_user_(*, session: Session = Depends(get_session), user: UserCreateRequest):
    ur = UserRepository()
    data = ur.create_user(session, user)
    if data is None:
        # The error Cannot create user does not give information why the creation failed
        return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"message": "Cannot create user"})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={})
