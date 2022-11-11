from fastapi import FastAPI
from api import api_router

"""
The main starting point for the fast api, which sets up the application.
"""

# REST API Settings
from config.models.ProjectSettings import ProjectSettings
from db.dbconfig import create_db_and_tables

app = FastAPI(title=ProjectSettings.PROJECT_NAME,
              description=ProjectSettings.PROJECT_DESCRIPTION,
              version=ProjectSettings.API_VERSION,
              openapi_url=f"{ProjectSettings.API_VERSION_PATH}/openapi.json",
              docs_url=f"{ProjectSettings.API_VERSION_PATH}/docs",
              redoc_url=f"{ProjectSettings.API_VERSION_PATH}/redoc")


# Router Inclusion
app.include_router(api_router, prefix=ProjectSettings.API_VERSION_PATH)


# Creating all necessary tables for SQL lite after the server starts
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
