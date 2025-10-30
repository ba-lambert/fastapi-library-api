from pydantic import BaseModel, EmailStr, ConfigDict

from app.enums.gender_enum import GenderEnum
from app.enums.role_enum import RoleEnum


class UserSignupSchema(BaseModel):
    username: str
    full_name: str | None = None
    email: EmailStr
    gender: GenderEnum
    password: str


class UserLoginSchema(BaseModel):
    username: str
    password: str

class UserResponseSchema(BaseModel):
    username:str
    email:str
    role:RoleEnum

    model_config = ConfigDict(from_attributes=True)