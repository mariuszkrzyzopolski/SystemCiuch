import datetime
import os
import sys

import jwt
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.authentication import AuthenticationError
from starlette.requests import Request

from API.database import DB, get_database
from Models.collection import Collection
from Models.user import User as Model_User
from Validators.user import User, UserLogin

sys.path.append("../")

conn = get_database()
database = DB(conn)
router = APIRouter(prefix="/user")


@router.post("/login")
def user_login(request: Request, user: UserLogin):
    with Session(database.conn) as session:
        data = (
            session.query(Model_User)
            .filter(Model_User.mail == user.mail, Model_User.password == user.password)
            .first()
        )
        if data is None:
            raise HTTPException(status_code=404, detail="User not found")
        elif data.password == user.password:
            request.session["user"] = data.id
            request.session["collection"] = data.collection.id
            exp = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(
                days=1
            )
            jwt_payload = jwt.encode({"exp": exp, "sub": data.id}, "secret")
            return {"token": jwt_payload, "expiresIn": exp}
        else:
            raise HTTPException(status_code=401, detail="Incorrect password")


@router.post("/register")
def user_register(request: Request, user: User):
    if user.password != user.repeated_password:
        raise HTTPException(status_code=401, detail="Passwords must be the identical!")
    with Session(database.conn) as session:
        q = select(Model_User).filter(Model_User.mail == user.mail)
        if session.execute(q).first() is not None:
            raise HTTPException(status_code=400, detail="mail already registered")
        new_user = Model_User(mail=user.mail, password=user.password, city=user.city)
        request.session["user"] = new_user.id
        new_collection = Collection(user=new_user)
        new_user.collection = new_collection
        session.add(new_collection)
        session.commit()
        if not os.path.exists(f"images/{new_collection.id}"):
            os.makedirs(f"images/{new_collection.id}")
        request.session["collection"] = new_collection.id
        exp = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(
            days=1
        )
        jwt_payload = jwt.encode({"exp": exp, "sub": new_user.id}, "secret")
        return {"token": jwt_payload, "expiresIn": exp}


@router.post("/refresh")
def refresh_token(request: Request):
    try:
        exp = datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(
            days=1
        )
        jwt_payload = jwt.encode({"exp": exp, "sub": request.session["user"]}, "secret")
        return {"token": jwt_payload, "expiresIn": exp}
    except AuthenticationError:
        raise HTTPException(status_code=403, detail="Invalid token!")


@router.post("/logout")
def logout(request: Request):
    del request.session["user"]
    return {"success": True}
