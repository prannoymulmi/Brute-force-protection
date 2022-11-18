from fastapi.testclient import TestClient
from sqlmodel import Session
from starlette import status

from config.models.ProjectSettings import ProjectSettings
from db.models import Staff
from schemas.TokenResponse import TokenResponse
from tests.testutils import TestUtils
from utils.jwt_utils import decode_jwt


def test_authenticate_users_when_authenticate_with_correct_credentials_then_request_is_successful(session: Session,
                                                                                                  client: TestClient):
    # Given
    password, username = create_user(session)

    # When
    response = client.post(f"{ProjectSettings.API_VERSION_PATH}/authenticate",
                           json={"username": username, "password": password})

    # Then
    assert response.status_code == status.HTTP_200_OK
    assert response.json() is not None


def test_authenticate_users_when_authenticate_with_login_attempts_exceeded_then_request_is_forbidden(session: Session,
                                                                                                     client: TestClient):
    # Given
    username = "testUser"
    password = "test"
    user = Staff(username=username, password=password, email="test@test", login_counter=5)
    TestUtils.add_user_to_in_mem_db(user, session)

    # When
    # Correct credentials are provided
    response = client.post(f"{ProjectSettings.API_VERSION_PATH}/authenticate",
                           json={"username": username, "password": password})

    # Then
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {"message": "Staff is blocked due to too many attempts"}


def test_authenticate_users_when_authenticate_with_wrong_credentials_then_request_is_unauthorized_and_counter_is_incremented(
        session: Session,
        client: TestClient):
    # Given
    _, username = create_user(session)

    # When
    # Correct credentials are provided
    user = session.get(Staff, username)
    assert user.login_counter == 0
    response = client.post(f"{ProjectSettings.API_VERSION_PATH}/authenticate",
                           json={"username": username, "password": "wrongPassword"})

    saved_user_attempt_1 = session.get(Staff, username)

    # Then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"message": "Username or Password is incorrect"}
    assert saved_user_attempt_1.login_counter == 1

    # Attempt another wrong login to assert the counter
    response_incorrect_attempt_2 = client.post(f"{ProjectSettings.API_VERSION_PATH}/authenticate",
                                               json={"username": username, "password": "wrongPassword"})

    saved_user_attempt_2 = session.get(Staff, username)

    assert saved_user_attempt_2.login_counter == 2
    assert response_incorrect_attempt_2.status_code == status.HTTP_401_UNAUTHORIZED
    assert response_incorrect_attempt_2.json() == {"message": "Username or Password is incorrect"}


"""
Checks if counter is incremented after a wrong attempt and also the counter is reset after correct attempt
"""


def test_authenticate_users_when_authenticate_with_wrong_credentials_once_then_request_is_unauthorized_and_counter_is_incremented_and_then_reseted(
        session: Session,
        client: TestClient):
    # Given
    password, username = create_user(session)

    # When
    # Correct credentials are provided
    user = session.get(Staff, username)
    assert user.login_counter == 0
    response = client.post(f"{ProjectSettings.API_VERSION_PATH}/authenticate",
                           json={"username": username, "password": "wrongPassword"})

    saved_user_attempt_1 = session.get(Staff, username)

    # Then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"message": "Username or Password is incorrect"}
    assert saved_user_attempt_1.login_counter == 1

    # Attempt another wrong login to assert the counter
    response_correct_attempt = client.post(f"{ProjectSettings.API_VERSION_PATH}/authenticate",
                                           json={"username": username, "password": password})

    saved_user_attempt_2 = session.get(Staff, username)

    token: TokenResponse = TokenResponse.parse_raw(response_correct_attempt.json())
    assert saved_user_attempt_2.login_counter == 0
    assert response_correct_attempt.status_code == status.HTTP_200_OK
    assert token.token is not None
    assert decode_jwt(token.token) is not None



def test_authenticate_users_when_authenticate_with_wrong_credentials_exceeded_then_request_is_unauthorized_and_counter_is_incremented(
        session: Session,
        client: TestClient):
    # Given
    _, username = create_user(session)

    # When
    # Correct credentials are provided
    user = session.get(Staff, username)
    assert user.login_counter == 0
    response = client.post(f"{ProjectSettings.API_VERSION_PATH}/authenticate",
                           json={"username": username, "password": "wrongPassword"})

    saved_user_attempt_1 = session.get(Staff, username)

    # Then
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {"message": "Username or Password is incorrect"}
    assert saved_user_attempt_1.login_counter == 1

    # Attempt another wrong login to assert the counter
    client.post(f"{ProjectSettings.API_VERSION_PATH}/authenticate",
                json={"username": username, "password": "wrongPassword"})

    saved_user_attempt_2 = session.get(Staff, username)

    assert saved_user_attempt_2.login_counter == 2


def test_authenticate_users_when_authenticate_with_incorrect_credentials_then_request_is_unauthorized(
        client: TestClient):
    response = client.post(f"{ProjectSettings.API_VERSION_PATH}/authenticate",
                           json={"username": "testUser", "password": "wrongPassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {'message': 'Username or Password is incorrect'}


def test_authenticate_users_when_authenticate_with_large_input_password_then_unprocessable_request_is_returned(
        client: TestClient):
    response = client.post(f"{ProjectSettings.API_VERSION_PATH}/authenticate", json={"username": "testUser",
                                                                                     "password": "longlonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglonglongPassword"})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert response.json() == {'detail': [{'ctx': {'limit_value': 64},
                                           'loc': ['body', 'password'],
                                           'msg': 'ensure this value has at most 64 characters',
                                           'type': 'value_error.any_str.max_length'}]}


def create_user(session):
    username = "testUser"
    password = "test"
    user = Staff(username=username, password=password, email="test@test")
    TestUtils.add_user_to_in_mem_db(user, session)
    return password, username
