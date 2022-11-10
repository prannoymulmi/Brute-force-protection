from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# REST API Settings
from config.models.ProjectSettings import ProjectSettings

from api import api_router
from db.dbconfig import create_db_and_tables
from exceptions.UserNotFoundError import UserNotFoundError
from middleware.generic_error_handler import unauthorized_exception_handler

app = FastAPI(title=ProjectSettings.PROJECT_NAME,
              description=ProjectSettings.PROJECT_DESCRIPTION,
              version="1.0.0",
              # docs_url=None,
              # redoc_url=None,
              openapi_url=f"{ProjectSettings.API_VERSION_PATH}/openapi.json",
              docs_url=f"{ProjectSettings.API_VERSION_PATH}/docs",
              redoc_url=f"{ProjectSettings.API_VERSION_PATH}/redoc")

# Middleware Settings
# Used when there is a ASMIS frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["GET, POST"],
)

# Router Inclusion
app.include_router(api_router, prefix=ProjectSettings.API_VERSION_PATH)


# Creating all necessary tables for SQL lite after the server starts
@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# Exception handling Inclusion
#app.add_exception_handler(UserNotFoundError, unauthorized_exception_handler)
