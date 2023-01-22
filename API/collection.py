from typing import List, Union

from fastapi import Form, APIRouter, HTTPException, File, UploadFile
from pydantic import BaseModel
from pydantic.class_validators import Optional

router = APIRouter()
class Shelf(BaseModel):
    name: str
    clothing_items: List

shelves = dict()
database = dict()

@router.post("/sets/{set_id}")
async def post_set(set_id):
    return {}


@router.get("/sets/{set_id}")
async def get_set(set_id):
    return {}
@router.post("/items")
async def post_item(
        name:str = Form(...),
        type: str = Form(...),
        description: str = Form(...),
        image: UploadFile = File(...)
):
    database[name] = {"name":name,"type":type,"description":description,"image":image.filename}
    return {"Form":{"name":name,"type":type,"description":description},"image":image.filename}


@router.get("/items/{item_id}")
async def get_item(item_name):
    return {"item": database[item_name]}

# @router.put("/shelves/{shelf_id}")
# async def put_item_on_shelf(shelf_id: int, clothing_items: List):
#     if shelf_id not in shelves:
#         raise HTTPException(status_code=404, detail="Shelf not found")
#     shelves[shelf_id].clothing_items = clothing_items
#     return {"success": True}