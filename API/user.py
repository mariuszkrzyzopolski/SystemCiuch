import sys

sys.path.append('../')
from Models.user import User

from typing import List
from urllib import request
from fastapi import APIRouter, FastAPI, HTTPException

router = APIRouter()

database = {}


@router.post("/login")
async def user_login(user: User):
    if database[user.mail].password == user.password:
        return {"success": True}
    else:
        raise HTTPException(status_code=401, detail="Incorrect password")
    # else:
    #     raise HTTPException(status_code=404, detail="User not found")


@router.post("/register")
async def user_register(user: User):
    if user.mail in database:
        raise HTTPException(status_code=400, detail="Username already taken")
    database[user.mail] = user
    return {"success": True}


@router.post("/logout")
async def logout():
    # Remove the logged in user from the session
    del database[request.user.mail]
    return {"success": True}


@router.post("/connect")
async def user_connect():
    return {}
