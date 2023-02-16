from typing import List, Union

from fastapi import Form, APIRouter, HTTPException, File, UploadFile
from pydantic.class_validators import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session

from API.database import get_database, DB
from Models.collection import Collection
from Models.item import Item
from Models.set import Set
from Models.wardrobe import Wardrobe

conn = get_database()
database = DB(conn)
router = APIRouter()

# TODO Patch for sets and items
@router.post("/set")
async def post_set():
    return {}


@router.get("/sets/{set_id}")
async def get_set(set_id):
    return {}

@router.get("/sets")
async def get_sets():
    with Session(database.conn) as session:
        q = select(Set)
        data = session.execute(q).all()
        return data

@router.get("/sets_with_item/{item_id}")
async def get_sets_with_item(item_id):
    return {}
@router.post("/item")
async def post_item(
    type: str = Form(...),
    description: str = Form(None),
    tags: List[str] = Form(...),
    image: UploadFile = File(...)
):
    with Session(database.conn) as session:
        # TODO add collection id, preferably from session
        item = Item(type=type, description=description, tags=','.join(tags), image=image.filename)
        session.add(item)
        session.commit()
        session.refresh(item)
        return item #{"Form":{"tags":tags,"type":type,"description":description},"image":image.filename}

@router.get("/items")
async def get_items():
    # Need user id to retrieve list
    with Session(database.conn) as session:
        s = select(Wardrobe)
        q = select(Item)
        data = session.execute(q).all()
        return data
@router.get("/items/{item_id}")
async def get_item(item_name):
    return {}

@router.get("/")
async def get_collection():
    # Need user id to retrieve list
    with Session(database.conn) as session:
        q = select(Collection)
        data = session.execute(q).all()
        return data