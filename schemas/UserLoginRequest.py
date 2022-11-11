from pydantic import BaseModel, Field

'''
Inheriting BaseModel from pydantic, because it has all the methods needed for a schema, i.e, to_json, validate etc. 
'''


class UserLoginRequest(BaseModel):
    username: str = Field(
        max_length=64
    )
    # Owasp recommends max length of 64 chars because it is supported by most of the hashing algorithms
    # <a href=https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/Authentication_Cheat_Sheet.md#authentication-solution-and-sensitive-account> see for more details
    password: str = Field(
        title="Password for a user", max_length=64
    )
