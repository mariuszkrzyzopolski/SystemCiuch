import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

import API.collection as collection
import Common.user_functions as ufunc
from API.database import DB, get_database
from Models.user import User
from Models.wardrobe import Wardrobe
from Validators.user import WardrobeCode, WardrobeLogin

conn = get_database()
database = DB(conn)
router = APIRouter(prefix="/wardrobe")


@router.post("/connect")
def user_connect(
    wardrobe_code: WardrobeCode, user: User = Depends(ufunc.get_current_user)
):
    with Session(database.conn) as session:
        q = select(Wardrobe).filter(
            Wardrobe.mail == user.mail and Wardrobe.password == wardrobe_code
        )
        if session.execute(q).first() is not None:
            raise HTTPException(status_code=400, detail="Wardrobe already registered")
        new_wardrobe = Wardrobe(
            mail=user.mail, password=wardrobe_code.wardrobe_code, user=user
        )
        session.add(new_wardrobe)
        session.commit()
        return new_wardrobe


@router.delete("/disconnect")
def user_disconnect(user: User = Depends(ufunc.get_current_user)):
    with Session(database.conn) as session:
        data = session.query(Wardrobe).filter(Wardrobe.id == user.id_wardrobe).first()
        if data is not None:
            wardrobe = session.get(Wardrobe, user.id_wardrobe)
            session.delete(wardrobe)
            session.commit()
        else:
            raise HTTPException(status_code=404, detail="Wardrobe not found")
        return {}


@router.post("/login_wardrobe")
def wardrobe_login(wardrobe: WardrobeLogin):
    with Session(database.conn) as session:
        data = session.query(Wardrobe).filter(Wardrobe.mail == wardrobe.mail).first()
        if data is None:
            raise HTTPException(status_code=404, detail="Wardrobe not found")
        elif data.password == wardrobe.password:
            access_token = ufunc.create_access_token(
                data={"sub": data.id}, expires_delta=datetime.timedelta(days=1)
            )
            return {"token": access_token, "expiresIn": ufunc.expires_in(1)}
        else:
            raise HTTPException(status_code=401, detail="Incorrect password")


@router.get("/items")
def get_items(wardrobe: Wardrobe = Depends(ufunc.get_current_user)):
    with Session(database.conn) as session:
        user = session.query(User).filter(User.mail == wardrobe.mail).first()
        items = collection.get_items(user)
    return items
