from fastapi import APIRouter

router = APIRouter(prefix="/ai")


@router.post("/predict")
def predict():
    return {}


@router.get("/train")
def train():
    return {}
