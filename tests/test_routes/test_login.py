from contextlib import contextmanager

import pytest
from argon2 import PasswordHasher
from fastapi.testclient import TestClient
from starlette import status
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, create_engine
from db import models, dbconfig
from config.models.ProjectSettings import ProjectSettings
from db.models import User
from main import app

"""
Start Initializing Test with data in the in memory database
"""


@pytest.fixture(name="session", autouse=True)
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    models.SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def session_scope_override():
        return session  #

    app.dependency_overrides[dbconfig.get_session] = session_scope_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


"""
END
"""


def test_authenticate_users_when_authenticate_with_correct_credentials_then_request_is_successful(session: Session,
                                                                                                  client: TestClient):
    # Given
    username = "testUser"
    password = "test"
    add_user_to_in_mem_db(password, session, username)

    # When
    response = client.post(f"{ProjectSettings.API_VERSION_PATH}/authenticate",
                           json={"username": username, "password": password})

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'token': 'hello'}


def add_user_to_in_mem_db(password, session, username):
    ph = PasswordHasher()
    hashed_pw = ph.hash(password)
    user = User(username=username, password=hashed_pw)
    session.add(user)
    session.commit()


def test_authenticate_users_when_authenticate_with_incorrect_credentials_then_request_is_unauthorized(
        client: TestClient):
    response = client.post(f"{ProjectSettings.API_VERSION_PATH}/authenticate",
                           json={"username": "testUser", "password": "wrongPassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'message': 'Oops! unauthorized'}


def test_authenticate_users_when_authenticate_with_large_input_password_then_unprocessable_request_is_returned(
        client: TestClient):
    response = client.post(f"{ProjectSettings.API_VERSION_PATH}/authenticate", json={"username": "testUser",
                                                                                     "password": "longlonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglongPassword"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {'detail': [{'ctx': {'limit_value': 64},
                                           'loc': ['body', 'password'],
                                           'msg': 'ensure this value has at most 64 characters',
                                           'type': 'value_error.any_str.max_length'}]}
