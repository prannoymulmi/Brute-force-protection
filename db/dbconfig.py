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
A reusable method which returns a session for the database. This session can be used to execute queries from the functions. 
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

