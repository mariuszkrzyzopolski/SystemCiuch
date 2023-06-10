from pydantic import BaseModel
from pydantic.fields import Optional


class User(BaseModel):
    mail: str
    city: str
    password: str
    repeated_password: str


class UserLogin(BaseModel):
    mail: str
    password: str


class EditUser(BaseModel):
    mail: Optional[str]
    city: Optional[str]
    password: Optional[str]


class WardrobeLogin(BaseModel):
    mail: str
    password: str


class WardrobeCode(BaseModel):
    wardrobe_code: str
