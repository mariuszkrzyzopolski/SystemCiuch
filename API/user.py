import sys

from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.requests import Request

from API.database import get_database, DB

sys.path.append('../')
from Validators.user import User
from Models.user import User as Model_User
from fastapi import APIRouter, HTTPException

conn = get_database()
database = DB(conn)
router = APIRouter()

@router.post("/login")
def user_login(request: Request, mail: str, password: str):
    with Session(database.conn) as session:
        data = session.query(Model_User).filter(Model_User.mail == mail, Model_User.password == password).first()
        if data is None:
            raise HTTPException(status_code=404, detail="User not found")
        elif data.password == password:
            request.session["user"] = data.id
            return {"success": True}
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
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        request.session["user"] = new_user.id
        return new_user


@router.post("/logout")
def logout(request: Request):
    del request.session["user"]
    return {"success": True}
