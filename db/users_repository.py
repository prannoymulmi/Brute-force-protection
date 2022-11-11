from datetime import datetime
from typing import Any

from argon2 import PasswordHasher
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select, Session

from db import models
from db.models import User
from exceptions.UserNotFoundError import UserNotFoundError
from schemas.UserCreateRequest import UserCreateRequest


class UserRepository:

    def create_user(self: str, session: Session, user: UserCreateRequest) -> Any:
        """ Add New User"""

        if self.__check_if_user_exists(session, user):
            return None
        try:
            ph = PasswordHasher()
            hashed_password = ph.hash(user.password)
            db_user = User(username=user.username,
                           password=hashed_password,
                           email=user.email
                           )
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return db_user
        except SQLAlchemyError as e:
            # logger.info(e)
            return None

    def increment_login_counter_for_user(self, session: Session, username: str):
        user = self.get_user_with_username(session, username)
        user.login_counter = user.login_counter + 1
        user.modified_timestamp = datetime.utcnow()
        session.add(user)
        session.commit()
        session.refresh(user)

    def reset_login_counter_for_user(self, session: Session, username: str):
        user = self.get_user_with_username(session, username)
        user.login_counter = 0
        user.modified_timestamp = datetime.utcnow()
        session.add(user)
        session.commit()
        session.refresh(user)

    def get_user_with_username(self, session, username):
        statement = select(User).where(User.username == username)
        results = session.exec(statement)
        user = results.one()
        return user

    def get_user_id(self, session: Session, username: str) -> Any:
        """ Get User Data based on name"""
        try:
            statement = select(models.User).where(
                models.User.username == username)
            result = session.exec(statement)
            data = result.one()
            return data
        except SQLAlchemyError as e:
            raise UserNotFoundError(f"User not found {e}")

    def __check_if_user_exists(self, session: Session, user: UserCreateRequest) -> bool:
        try:
            self.get_user_id(session, user.username)
            return True
        except UserNotFoundError:
            return False
