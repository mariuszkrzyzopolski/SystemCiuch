from fastapi import APIRouter

router = APIRouter()


@router.post("/predict")
async def predict():
    return {}


@router.get("/train")
async def train():
    return {}
