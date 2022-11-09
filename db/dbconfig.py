from sqlmodel import Session, create_engine, SQLModel
from contextlib import contextmanager

from config.models.DBSettings import DBSettings
from . import models

engine = create_engine(
    DBSettings.DB_URL,
    echo=True
)

models.SQLModel.metadata.create_all(engine)


"""
Using contextmanager to reuse the opening and closing of db session
"""


@contextmanager
def session_scope() -> Session:
    """Provide a transactional scope around a series of operations."""
    db = None
    try:
        db = Session(autocommit=False, autoflush=False,
                     bind=engine)  # create session from SQLModel session
        yield db
    finally:
        db.close()

