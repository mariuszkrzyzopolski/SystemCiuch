import sys

from fastapi import APIRouter, Depends

from API.database import DB, get_database
from Common.user_functions import get_current_user
from Models.user import User

sys.path.append("../")
conn = get_database()
database = DB(conn)
router = APIRouter(prefix="/wardrobe")


@router.post("/connect")
def user_connect(wadrobe_code: int, user: User = Depends(get_current_user)):
    return {}


@router.post("/disconnect")
def user_disconnect(user: User = Depends(get_current_user)):
    return {"success": True}
