import sys

from fastapi import APIRouter
from starlette.requests import Request

from API.database import DB, get_database

sys.path.append("../")
conn = get_database()
database = DB(conn)
router = APIRouter(prefix="/wardrobe")


@router.post("/connect")
def user_connect(request: Request, wadrobe_code: int):
    return {}


@router.post("/disconnect")
def user_disconnect(request: Request):
    return {"success": True}
