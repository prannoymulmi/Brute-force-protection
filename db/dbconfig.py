from sqlmodel import Session, create_engine

from config.models.DBSettings import DBSettings
from . import models

engine = create_engine(
    DBSettings.DB_URL,
    connect_args={'check_same_thread': False},
    echo=True
)


def create_db_and_tables():
    models.SQLModel.metadata.create_all(engine)


"""
Using contextmanager to reuse the opening and closing of db session
"""


def get_session() -> Session:
    """Provide a transactional scope around a series of operations."""
    db = None
    try:
        db = Session(autocommit=False, autoflush=False,
                     bind=engine)  # create session from SQLModel session
        yield db
    finally:
        db.close()

