from fastapi import APIRouter
from . import login
from . import account_creation

api_router = APIRouter()

api_router.include_router(login.router, tags=["Login"])
api_router.include_router(account_creation.router, tags=["Account Creation"])