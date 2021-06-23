from typing import Optional, List
from pydantic import BaseModel


class User(BaseModel):
    username: str
    full_name: Optional[str] = None
    email: Optional[str] = None
    access_level: Optional[int] = None
    password: Optional[bool] = None
    disabled: Optional[bool] = None


class UserInsert(BaseModel):
    username: str
    full_name: str
    email: str
    access_level: int
    password: str
    disabled: bool


class SchemaUser(BaseModel):
    schemas_user: UserInsert
