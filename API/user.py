import sys

from sqlalchemy import select
from sqlalchemy.orm import Session

from API.database import get_database, DB

sys.path.append('../')
from Validators.user import User
from Models.user import User as Model_User

from typing import List
from urllib import request
from fastapi import APIRouter, FastAPI, HTTPException

conn = get_database()
database = DB(conn)
router = APIRouter()

@router.post("/login")
async def user_login(user: User):
    with Session(database.conn) as session:
        q = select(Model_User)
        data = session.execute(q).first()
        if data[user.mail].password == user.password:
            return {"success": True}
        else:
            raise HTTPException(status_code=401, detail="Incorrect password")
    # else:
    #     raise HTTPException(status_code=404, detail="User not found")


# @router.post("/register")
# async def user_register(user: User):
#     if user.mail in database:
#         raise HTTPException(status_code=400, detail="Username already taken")
#     database[user.mail] = user
#     return {"success": True}


@router.post("/logout")
async def logout():
    del database[request.user.mail]
    return {"success": True}


@router.post("/connect")
async def user_connect():
    return {}
