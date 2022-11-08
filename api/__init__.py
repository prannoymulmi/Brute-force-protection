from fastapi import APIRouter
from . import login
from . import test

api_router = APIRouter()

api_router.include_router(login.router, tags=["Login"])
api_router.include_router(test.router, tags=["Test"])