from datetime import datetime
from typing import Any

from argon2 import PasswordHasher
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select, Session

from db import models
from db.models import Staff
from exceptions.CannotCreateUserError import CannotCreateUserError
from exceptions.UserNotFoundError import UserNotFoundError
from schemas.StaffUserCreateRequest import StaffUserCreateRequest


class UserRepository:
    """ A method which creates a staff if it does not exist"""
    def create_user_or_else_return_none(self: str, session: Session, user: StaffUserCreateRequest) -> Any:
        # does nothing if a staff already exists
        if self.__check_if_user_exists(session, user):
            return None
        try:
            ph = PasswordHasher()
            # hashes the password into argon2id with random salt
            hashed_password = ph.hash(user.password)
            db_user = Staff(username=user.username,
                            password=hashed_password,
                            email=user.email
                            )
            # the staff is then saved in the database using the orm
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return db_user
        except SQLAlchemyError:
            """
            Following Owasp, the error does not give away vital information outside that the email or username already exists.
            https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/Authentication_Cheat_Sheet.md#authentication-and-error-messages
            """
            raise CannotCreateUserError(f"Cannot create staff")

    """
    Method which increases the counter when there is a failed login attempt for the staff
    """
    def increment_login_counter_for_user(self, session: Session, username: str):
        user = self.get_user_with_username(session, username)
        user.login_counter = user.login_counter + 1
        user.modified_timestamp = datetime.utcnow()
        session.add(user)
        session.commit()
        session.refresh(user)

    """
       Method which resets the counter to 0, when there is a failed login attempt for the staff
    """
    def reset_login_counter_for_user(self, session: Session, username: str):
        user = self.get_user_with_username(session, username)
        user.login_counter = 0
        user.modified_timestamp = datetime.utcnow()
        session.add(user)
        session.commit()
        session.refresh(user)

    def get_user_with_username(self, session, username):
        statement = select(Staff).where(Staff.username == username)
        results = session.exec(statement)
        user = results.one()
        return user

    """ Get Staff Data based on name"""
    def get_user_id(self, session: Session, username: str) -> Any:
        try:
            statement = select(models.Staff).where(
                models.Staff.username == username)
            result = session.exec(statement)
            data = result.one()
            return data
        except SQLAlchemyError as e:
            raise UserNotFoundError(f"Staff not found {e}")

    """A private method, which checks if the staff exists"""
    def __check_if_user_exists(self, session: Session, user: StaffUserCreateRequest) -> bool:
        try:
            self.get_user_id(session, user.username)
            return True
        except UserNotFoundError:
            return False
