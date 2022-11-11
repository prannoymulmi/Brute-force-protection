import pytest
from argon2 import PasswordHasher
from sqlmodel import Session

from db.models import User
from db.users_repository import UserRepository
from exceptions.UserNotFoundError import UserNotFoundError
from schemas.UserCreateRequest import UserCreateRequest
from tests.testutils import TestUtils


def test_create_user_when_user_does_not_exists_then_new_user_is_created(session: Session):
    # Given
    ur = UserRepository()
    user: UserCreateRequest = UserCreateRequest(username="test", password="test", email="test@test")

    # When
    data: User = ur.create_user(session, user)

    # Then
    assert data.username == "test"


def test_create_user_when_user_does_not_exists_then_password_is_stored_as_a_hash_in_the_db(session: Session):
    # Given
    ur = UserRepository()
    user: UserCreateRequest = UserCreateRequest(username="test", password="test", email="test@test")

    # When
    data: User = ur.create_user(session, user)

    # Then
    ph = PasswordHasher()
    assert ph.verify(data.password, "test")


def test_create_user_when_user_does_not_exists_then_new_user_is_not_created_twice(session: Session):
    # Given
    ur = UserRepository()
    username = "test"
    password = "test"
    user_initial = User(username=username, password=password, email="test@test")
    TestUtils.add_user_to_in_mem_db(user_initial, session)
    user: UserCreateRequest = UserCreateRequest(username="test", password="test", email="test@test")

    # When
    data = ur.create_user(session, user)

    # Then
    assert data is None


def test_get_user_when_user_exists_then_user_is_returned(session: Session):
    # Given
    ur = UserRepository()
    username = "test"
    password = "test"
    user = User(username=username, password=password, email="test@test")
    TestUtils.add_user_to_in_mem_db(user, session)

    # When
    data: User = ur.get_user_id(session, username)

    # Then
    ph = PasswordHasher()
    assert data is not None
    assert ph.verify(data.password, password)
    assert data.created_timestamp is not None
    assert data.email == "test@test"


def test_get_user_when_does_not_user_exists_then_user_not_found_error_raised(session: Session):
    # Given
    ur = UserRepository()
    username = "nonExistingUser"

    # When and then
    with pytest.raises(UserNotFoundError):
        ur.get_user_id(session, username)
