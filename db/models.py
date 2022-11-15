from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlmodel import Field
from sqlmodel import SQLModel

""" The database models, which the ORM uses to translate data into tables."""
class Staff(SQLModel, table=True):
    username: str = Field(primary_key=True, index=True)
    email: str = Field(sa_column=Column(String, unique=True, index=True, nullable=False))
    password: str = Field(nullable=False)
    modified_timestamp: datetime = Field(
        sa_column=Column(DateTime, onupdate=datetime.now(), nullable=False, default=datetime.utcnow())
    )
    last_login_attempt: datetime = Field(default=datetime.utcnow())
    login_counter: int = Field(nullable=False, default=0)
    created_timestamp: datetime = Field(nullable=False,
                                        default=datetime.utcnow())
