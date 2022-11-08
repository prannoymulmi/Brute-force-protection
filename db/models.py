from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String
from sqlmodel import Field
from sqlmodel import SQLModel


class User(SQLModel, table=True):
    username: str = Field(primary_key=True, index=True)

    email: str = Field(sa_column=Column(String, unique=True, nullable=True))
    password: str = Field(nullable=False)
    created_timestamp: datetime = Field(nullable=False,
                                        default=datetime.utcnow())


class UserCounter(SQLModel, table=True):
    username: str = Field(primary_key=True, index=True)

    counter: Optional[int] = Field(sa_column=Column(String, unique=True, nullable=True))

    created_timestamp: datetime = Field(nullable=False,
                                        default=datetime.utcnow())
