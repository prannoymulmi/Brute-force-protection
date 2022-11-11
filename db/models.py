from datetime import datetime
from sqlalchemy import Column, String
from sqlmodel import Field
from sqlmodel import SQLModel

""" The database models, which the ORM uses to translate data into tables."""
class User(SQLModel, table=True):
    username: str = Field(primary_key=True, index=True)

    email: str = Field(sa_column=Column(String, unique=True, nullable=False))
    password: str = Field(nullable=False)
    modified_timestamp: datetime = Field(nullable=False,
                                         default=datetime.utcnow())
    login_counter: int = Field(nullable=False, default=0)
    created_timestamp: datetime = Field(nullable=False,
                                        default=datetime.utcnow())

