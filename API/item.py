from typing import List

from fastapi import Form, APIRouter, File, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

import AI.remove_background as ai
import Common.image_functions as fimg
from API.database import get_database, DB
from Models.item import Item
from starlette.requests import Request

conn = get_database()
database = DB(conn)
router = APIRouter()


@router.post("/")
def post_item(
    request: Request,
    type: str = Form(...),
    description: str = Form(None),
    tags: List[str] = Form(...),
    image: UploadFile = File(...)
):
    with Session(database.conn) as session:
        extension = image.filename.split(".")[-1] in ("jpg", "jpeg", "png")
        if not extension:
            return "Image must be jpg or png format!"
        if extension == "png":
            image = fimg.png_to_jpg(image)
        cv2_img = fimg.api_to_cv2(image)
        cv2_img = fimg.resize_cv(cv2_img)
        cv2_img = ai.cv2_remove_backgound(cv2_img)
        image = fimg.cv2_to_pil(cv2_img)

        item = Item(type=type, description=description, tags=','.join(tags), image=image.filename,
                    collection_id=request.session["collection"])
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
