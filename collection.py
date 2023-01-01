from typing import List

from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel

router = APIRouter()

class Item(BaseModel):
    name: str
    type: str
    description: str
    image: str

class Shelf(BaseModel):
    name: str
    clothing_items: List[Item]

shelves = {}
database = {}

@router.post("/sets/{set_id}")
async def post_set(set_id):
    return {}


@router.get("/sets/{set_id}")
async def get_set(set_id):
    return {}

def get_empty_shelve():
    return next(x for x in shelves if len(x) == 0)
@router.post("/items/{item_id}")
async def post_item(item: Item):
    database[item.name] = item
    shelves[get_empty_shelve().name] = item
    return {"success": True}


@router.get("/items/{item_id}")
async def get_item(item_name):
    return {"item": database[item_name]}

@router.put("/shelves/{shelf_id}")
async def put_item_on_shelf(shelf_id: int, clothing_items: List[Item]):
    if shelf_id not in shelves:
        raise HTTPException(status_code=404, detail="Shelf not found")
    shelves[shelf_id].clothing_items = clothing_items
    return {"success": True}