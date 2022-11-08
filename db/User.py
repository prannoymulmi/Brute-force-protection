from pydantic import BaseModel
from typing import Union


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    hashed_password: str
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None
