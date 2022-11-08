from fastapi.testclient import TestClient
from starlette import status

from config.models.ProjectSettings import ProjectSettings
from main import app

client = TestClient(app)


def test_authenticate_users_when_authenticate_with_correct_credentials_then_request_is_successful():
    response = client.post(f"{ProjectSettings.API_VERSION_PATH}/authenticate",
                           json={"username": "testUser", "password": "test"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'token': 'hello'}


def test_authenticate_users_when_authenticate_with_incorrect_credentials_then_request_is_unauthorized():
    response = client.post(f"{ProjectSettings.API_VERSION_PATH}/authenticate",
                           json={"username": "testUser", "password": "wrongPassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'message': 'Oops! unauthorized'}


def test_authenticate_users_when_authenticate_with_large_input_password_then_unprocessable_request_is_returned():
    response = client.post(f"{ProjectSettings.API_VERSION_PATH}/authenticate", json={"username": "testUser",
                                                                                     "password": "longlonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglongPassword"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {'detail': [{'ctx': {'limit_value': 64},
                                           'loc': ['body', 'password'],
                                           'msg': 'ensure this value has at most 64 characters',
                                           'type': 'value_error.any_str.max_length'}]}
