import uvicorn as uvicorn
from fastapi import FastAPI
import collection
import user
import ai_model

app = FastAPI()

app.include_router(collection.router, prefix="/collection", tags=["collection"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(ai_model.router, prefix="/ai", tags=["ai"])

if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, log_level="info")
