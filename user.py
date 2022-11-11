from fastapi import APIRouter

router = APIRouter()


@router.post("/login")
async def user_login():
    return {}


@router.post("/register")
async def user_register():
    return {}


@router.post("/logout")
async def user_logout():
    return {}


@router.post("/connect")
async def user_connect():
    return {}
