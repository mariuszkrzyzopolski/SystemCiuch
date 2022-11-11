from fastapi import APIRouter

router = APIRouter()


@router.post("/sets/{set_id}")
async def post_set(set_id):
    return {}


@router.get("/sets/{set_id}")
async def get_set(set_id):
    return {}


@router.post("/items/{item_id}")
async def post_item(item_id):
    return {}


@router.get("/items/{item_id}")
async def get_item(item_id):
    return {}
