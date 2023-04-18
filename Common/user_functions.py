import datetime
from datetime import timedelta

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from typing_extensions import Type

from API.database import DB, get_database
from Models.user import User

conn = get_database()
database = DB(conn)

jwt_scheme = HTTPBearer()


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        exp = datetime.datetime.now(tz=datetime.timezone.utc) + expires_delta
    else:
        exp = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(
            days=1
        )
    to_encode.update({"exp": exp})
    jwt_payload = jwt.encode(to_encode, "secret", algorithm="HS256")
    return jwt_payload


class Token(BaseModel):
    access_token: str
    token_type: str


def expires_in(days: int):
    return datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(days=days)


def get_user(user_id: int) -> Type[User]:
    with Session(database.conn) as session:
        data = session.query(User).filter(User.id == user_id).first()
        return data


async def get_current_user(token: HTTPAuthorizationCredentials = Depends(jwt_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"Authenticate": "Bearer"},
    )
    payload = jwt.decode(token.credentials, "secret", algorithms=["HS256"])
    user: int = payload.get("sub")
    print(user)
    if user is None:
        raise credentials_exception
    auth_user = get_user(user_id=user)
    print(auth_user)
    if auth_user is None:
        raise credentials_exception
    return auth_user
