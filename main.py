import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# REST API Settings
from config.models.ProjectSettings import ProjectSettings

from api import api_router

app = FastAPI(title=ProjectSettings.PROJECT_NAME,
              description=ProjectSettings.PROJECT_DESCRIPTION,
              version="1.0.0",
              # docs_url=None,
              # redoc_url=None,
              openapi_url=f"{ProjectSettings.API_VERSION_PATH}/openapi.json",
              docs_url=f"{ProjectSettings.API_VERSION_PATH}/docs",
              redoc_url=f"{ProjectSettings.API_VERSION_PATH}/redoc")

# Middleware Settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:8080",
    ],
    allow_credentials=True,
)
app.include_router(api_router, prefix=ProjectSettings.API_VERSION_PATH)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8088, log_level='debug')