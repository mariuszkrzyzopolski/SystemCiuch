import os
import sys

from fastapi import APIRouter
from sqlalchemy.orm import Session
from starlette.requests import Request

from API.database import DB, get_database
from Models.collection import Collection
from Models.user import User as Model_User
from Models.wardrobe import Wardrobe

sys.path.append("../")
conn = get_database()
database = DB(conn)
router = APIRouter(prefix="/wardrobe")


@router.post("/connect")
def user_connect(request: Request, wadrobe_id: int):
    return {}


@router.post("/disconnect")
def user_disconnect(request: Request):
    del request.session["wardrobe"]
    return {"success": True}


@router.post("/register")
def register_wardrobe(request: Request):
    # TODO verification of user session
    with Session(database.conn) as session:
        new_wardrobe = Wardrobe(user_id=request.session["user"])
        session.add(new_wardrobe)
        session.commit()
        new_collection = Collection(
            id_wardrobe=new_wardrobe.id, id_user=request.session["user"]
        )
        session.add(new_collection)
        session.commit()
        session.refresh(new_wardrobe)
        new_wardrobe.id_collection = new_collection.id
        session.commit()
        session.refresh(new_wardrobe)
        user = session.query(Model_User).get(request.session["user"])
        user.id_wardrobe = new_wardrobe.id
        user.id_collection = new_collection.id
        session.commit()
        request.session["collection"] = new_collection.id
        if not os.path.exists(f"images/{new_collection.id}"):
            os.makedirs(f"images/{new_collection.id}")
        request.session["wardrobe"] = new_wardrobe.id
        return new_wardrobe
