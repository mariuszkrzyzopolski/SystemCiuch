from typing import List
from urllib import request

from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel


router = APIRouter()
class User(BaseModel):
    username: str
    password: str

database = {}
@router.post("/login")
async def user_login(user: User):
    if database[user.username].password == user.password:
        return {"success": True}
    else:
        raise HTTPException(status_code=401, detail="Incorrect password")
    # else:
    #     raise HTTPException(status_code=404, detail="User not found")


@router.post("/register")
async def user_register(user: User):
    if user.username in database:
        raise HTTPException(status_code=400, detail="Username already taken")
    database[user.username] = user
    return {"success": True}


@router.post("/logout")
async def logout():
    # Remove the logged in user from the session
    del database[request.user.username]
    return {"success": True}

@router.post("/connect")
async def user_connect():
    return {}


