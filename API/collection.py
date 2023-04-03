import datetime
from typing import List

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette.requests import Request

import AI.remove_background as ai
import Common.image_functions as fimg
from API.database import DB, get_database
from Models.collection import Collection
from Models.item import Item
from Models.set import Set

conn = get_database()
database = DB(conn)
router = APIRouter(prefix="/collection")


# TODO Patch for sets and items
@router.post("/set")
def post_set(top_id: int, pants_id: int, shoes_id: int):
    with Session(database.conn) as session:
        top = session.query(Item).get(top_id)
        pants = session.query(Item).get(pants_id)
        shoes = session.query(Item).get(shoes_id)
        new_set = Set(top=top, pants=pants, shoes=shoes)
        session.add(new_set)
        top.set_id = new_set.id
        pants.set_id = new_set.id
        shoes.set_id = new_set.id
        session.commit()
        session.refresh(new_set)
        return new_set


@router.get("/sets/{set_id}")
def get_set(set_id):
    with Session(database.conn) as session:
        q = select(Set).filter(Set.id == set_id)
        data = session.execute(q).mappings().first()
        return data


@router.get("/sets")
def get_sets():
    with Session(database.conn) as session:
        q = select(Set)
        data = session.execute(q).mappings().all()
        return data


@router.get("/")
def get_collection(request: Request):
    with Session(database.conn) as session:
        q = select(Collection).filter(Collection.id == request.session["collection"])
        data = session.execute(q).mappings().first()
        return data


@router.post("/item")
def post_item(
        request: Request,
        type: str = Form(...),
        description: str = Form(None),
        tags: List[str] = Form(...),
        image: UploadFile = File(...),
):
    with Session(database.conn) as session:
        extension = image.filename.split(".")[-1]
        if extension not in ("jpg", "jpeg", "png"):
            return HTTPException(
                status_code=400, detail="Image must be jpg or png format!"
            )
        if extension == "png":
            image = fimg.png_to_jpg(image)
        cv2_img = fimg.api_to_cv2(image)
        cv2_img = fimg.resize_cv(cv2_img)
        cv2_img = ai.cv2_remove_backgound(cv2_img)
        image = fimg.cv2_to_pil(cv2_img)
        new_filename = f"images/{request.session['collection']}/" \
                       f"{datetime.datetime.timestamp(datetime.datetime.now())}.{extension}"
        fimg.save_image(image, new_filename)

        item = Item(
            type=type,
            description=description,
            tags=",".join(tags),
            image=new_filename,
            collection_id=request.session["collection"],
        )
        session.add(item)
        session.commit()
        session.refresh(item)
        return item


@router.get("/items")
def get_items():
    with Session(database.conn) as session:
        q = select(Item)
        data = session.execute(q).mappings().all()
        return data


@router.get("/{item_id}")
def get_item(item_id):
    with Session(database.conn) as session:
        q = select(Item).filter(Item.id == item_id)
        data = session.execute(q).mappings().first()
        return data
