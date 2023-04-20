# isort: skip_file
import datetime
import os
import sys

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from API.database import DB, get_database
from Common.user_functions import create_access_token, expires_in, get_current_user
from Models.user import User as Model_User
from Validators.user import User, UserLogin

from Models.collection import Collection

sys.path.append("../")

conn = get_database()
database = DB(conn)
router = APIRouter(prefix="/user")


@router.post("/login")
def user_login(user: UserLogin):
    with Session(database.conn) as session:
        data = (
            session.query(Model_User)
            .filter(Model_User.mail == user.mail, Model_User.password == user.password)
            .first()
        )
        if data is None:
            raise HTTPException(status_code=404, detail="User not found")
        elif data.password == user.password:
            access_token = create_access_token(
                data={"sub": data.id}, expires_delta=datetime.timedelta(days=1)
            )
            return {"token": access_token, "expiresIn": expires_in(1)}
        else:
            raise HTTPException(status_code=401, detail="Incorrect password")


@router.post("/register")
def user_register(user: User):
    if user.password != user.repeated_password:
        raise HTTPException(status_code=401, detail="Passwords must be the identical!")
    with Session(database.conn) as session:
        q = select(Model_User).filter(Model_User.mail == user.mail)
        if session.execute(q).first() is not None:
            raise HTTPException(status_code=400, detail="mail already registered")
        new_user = Model_User(mail=user.mail, password=user.password, city=user.city)
        new_collection = Collection(user=new_user)
        new_user.collection = new_collection
        session.add(new_collection)
        session.commit()
        if not os.path.exists(f"../images/{new_collection.id}"):
            os.makedirs(f"../images/{new_collection.id}")
        access_token = create_access_token(
            data={"sub": new_user.id}, expires_delta=datetime.timedelta(days=1)
        )
        return {"token": access_token, "expiresIn": expires_in(days=1)}


@router.get("/current_user")
def authorized_user(user: User = Depends(get_current_user)):
    return user


@router.post("/logout")
def logout(user: User = Depends(get_current_user)):
    return {"success": True}
