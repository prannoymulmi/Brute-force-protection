from argon2 import PasswordHasher
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, create_engine

from db import models
from db.dbconfig import get_session
from db.models import User
from db.users_repository import UserRepository
from main import app


def test_create_user():
    engine = create_engine(
        # Using  https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/#configure-the-in-memory-database
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    models.SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        def session_scope_override():  #
            return session  #
        app.dependency_overrides[get_session] = session_scope_override
        ur = UserRepository()
        ur.create_user(session, "test", "test")
        data: User = ur.get_user_id(session, "test")
        app.dependency_overrides.clear()

        ph = PasswordHasher()
        assert data.username == "test"
        assert ph.verify(data.password, "test")
        # TODO: Assertions
