from fastapi import APIRouter

router = APIRouter()


@router.post("/predict")
def predict():
    return {}


@router.get("/train")
def train():
    return {}
