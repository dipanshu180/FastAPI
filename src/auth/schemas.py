from pydantic import BaseModel , Field
import uuid
from datetime import datetime


class UserCreateModel(BaseModel):
    first_name : str
    last_name : str
    username: str = Field(max_length=10)
    email: str = Field(max_length=255)
    password: str = Field(min_length=8)

class UserModel(BaseModel):
    uid: uuid.UUID
    username: str
    email: str
    password_hash: str = Field(exclude=True)
    first_name: str | None = None
    last_name: str | None = None
    is_verified: bool
    created_at: datetime
    update_at: datetime

class UserLoginModel(BaseModel):
    email: str = Field(max_length=255)
    password: str = Field(min_length=8)
