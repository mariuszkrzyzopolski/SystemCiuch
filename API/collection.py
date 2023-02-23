from typing import List

from fastapi import Form, APIRouter, File, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from API.database import get_database, DB
from Models.collection import Collection
from Models.item import Item
from Models.set import Set
from starlette.requests import Request

conn = get_database()
database = DB(conn)
router = APIRouter()

# TODO Patch for sets and items
@router.post("/set")
def post_set(top: int, pants: int, shoes: int):
    with Session(database.conn) as session:
        new_set = Set(top=top, pants=pants, shoes=shoes)
        session.add(new_set)
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

@router.post("/item")
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
@router.get("/items/{item_id}")
def get_item(item_id):
    with Session(database.conn) as session:
        q = select(Item).filter(Item.id == item_id)
        data = session.execute(q).mappings().first()
        return data

@router.get("/")
def get_collection(request: Request):
    with Session(database.conn) as session:
        q = select(Collection).filter(Collection.id == request.session["collection"])
        data = session.execute(q).mappings().first()
        return data