from pydantic import BaseModel


class User(BaseModel):
    mail: str
    city: str
    password: str
    repeated_password: str


class LoginUser(BaseModel):
    mail: str
    password: str
