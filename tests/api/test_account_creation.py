from unittest import mock
from unittest.mock import Mock

from sqlmodel import Session
from starlette import status
from starlette.testclient import TestClient

import utils
from config.models.ProjectSettings import ProjectSettings
from schemas.StaffUserCreateRequest import StaffUserCreateRequest
from utils.password_check import PasswordCheck

EMAIL = "test@test"

USERNAME = "test"
BAD_PASSWORD = "testPassword"
VALID_PASSWORD = "1VeryGoodPassword4All$%"
PASSWORD_LESS_THAN_8_CHARACTERS = "1God4$%"


def test_create_staff_user_when_password_policy_is_not_correct_then_a_bad_request_is_returned(session: Session,
                                                                                              client: TestClient):
    # Given
    user: StaffUserCreateRequest = StaffUserCreateRequest(username=USERNAME, password=BAD_PASSWORD, email=EMAIL)

    # When
    response = client.post(f"{ProjectSettings.API_VERSION_PATH}/addUser",
                           json=user.dict())

    # Then
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "message": "The password is not strong enough use at least 8 character, 2 Uppercase, 2 numbers, 2 specials, and 2 digits"}


def test_create_staff_user_when_password_policy_has_less_than_8_chars_then_a_bad_request_is_returned(session: Session,
                                                                                                      client: TestClient):
    # Given
    user: StaffUserCreateRequest = StaffUserCreateRequest(username=USERNAME, password=PASSWORD_LESS_THAN_8_CHARACTERS,
                                                          email=EMAIL)

    # When
    response = client.post(f"{ProjectSettings.API_VERSION_PATH}/addUser",
                           json=user.dict())

    # Then
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "message": "The password is not strong enough use at least 8 character, 2 Uppercase, 2 numbers, 2 specials, and 2 digits"}


def test_create_staff_user_when_password_has_all_requirements_is_not_correct_then_a_user_is_created(session: Session,
                                                                                                    client: TestClient):
    # Given
    PasswordCheck.check_compromised_password = Mock(return_value=False)
    user: StaffUserCreateRequest = StaffUserCreateRequest(username=USERNAME, password=VALID_PASSWORD, email=EMAIL)

    # When
    response = client.post(f"{ProjectSettings.API_VERSION_PATH}/addUser",
                           json=user.dict())

    # Then
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == {}


def test_create_staff_user_when_password_is_breached_then_400_is_returned(session: Session,
                                                                          client: TestClient):
    # Given
    PasswordCheck.check_compromised_password = Mock(return_value=True)
    user: StaffUserCreateRequest = StaffUserCreateRequest(username=USERNAME, password=VALID_PASSWORD, email=EMAIL)

    # When
    response = client.post(f"{ProjectSettings.API_VERSION_PATH}/addUser",
                           json=user.dict())

    # Then
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"message": "The Password has already been breached, please use another one"}


def test_create_staff_user_when_user_already_exists_then_forbidden_is_returned(session: Session,
                                                                               client: TestClient):
    # Given
    PasswordCheck.check_compromised_password = Mock(return_value=False)
    user: StaffUserCreateRequest = StaffUserCreateRequest(username=USERNAME, password=VALID_PASSWORD, email=EMAIL)

    # When
    response_success = client.post(f"{ProjectSettings.API_VERSION_PATH}/addUser",
                                   json=user.dict())
    # try to create the same staff again
    response_failure = client.post(f"{ProjectSettings.API_VERSION_PATH}/addUser",
                                   json=user.dict())

    # Then
    assert response_success.status_code == status.HTTP_201_CREATED
    assert response_success.json() == {}

    assert response_failure.status_code == status.HTTP_403_FORBIDDEN
    assert response_failure.json() == {"message": "Cannot create staff"}


def test_create_staff_user_when_email_already_exists_then_forbidden_is_returned(session: Session,
                                                                                client: TestClient):
    # Given
    PasswordCheck.check_compromised_password = Mock(return_value=False)
    user_1: StaffUserCreateRequest = StaffUserCreateRequest(username=USERNAME, password=VALID_PASSWORD, email=EMAIL)
    user_2: StaffUserCreateRequest = StaffUserCreateRequest(username="USERNAME", password=VALID_PASSWORD, email=EMAIL)

    # When
    response_success = client.post(f"{ProjectSettings.API_VERSION_PATH}/addUser",
                                   json=user_1.dict())
    # try to create the same staff again
    response_failure = client.post(f"{ProjectSettings.API_VERSION_PATH}/addUser",
                                   json=user_2.dict())

    # Then
    assert response_success.status_code == status.HTTP_201_CREATED
    assert response_success.json() == {}

    assert response_failure.status_code == status.HTTP_400_BAD_REQUEST
    assert response_failure.json() == {"message": "Cannot create staff"}
