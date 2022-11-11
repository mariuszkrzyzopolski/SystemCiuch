from fastapi import FastAPI
import collection
import user

app = FastAPI()

app.include_router(collection.router, prefix="/collection", tags=["collection"])
app.include_router(user.router, prefix="/user", tags=["user"])
