from typing import Any

from argon2 import PasswordHasher
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import select, Session
from db import models
from db.dbconfig import get_session
from db.models import User
from exceptions.UserNotFoundError import UserNotFoundError


class UserRepository:

    def create_user(self: str, session: Session, username: str, password: str) -> Any:
        """ Add New User"""
        ph = PasswordHasher()
        hashed_password = ph.hash(password)
        # logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
        # logger = logging.getLogger(__name__)
        try:
            db_user = User(username=username,
                           password=hashed_password,
                           )
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return db_user
        # with get_session() as db:
        # db_user = User(username=username,
        #                password=hashed_password,
        #                )
        # db.add(db_user)
        # db.commit()
        # db.refresh(db_user)
        # return db_user
        except SQLAlchemyError as e:
            # logger.info(e)
            return None

    def get_user_id(self, session: Session, username: str) -> Any:
        """ Get User Data based on name"""
        try:
            statement = select(models.User).where(
                models.User.username == username)
            result = session.exec(statement)
            data = result.one()
            return data
            # with get_session() as db:
            #     statement = select(models.User).where(
            #         models.User.username == username)
            #     results = db.exec(statement)
            #     data = results.one()
            #     return data
        except SQLAlchemyError as e:
            raise UserNotFoundError(f"User not found {e}")
