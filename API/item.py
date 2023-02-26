from typing import List

from fastapi import Form, APIRouter, File, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

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