import random

import uvicorn as uvicorn
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
import ai_model
from API import user, collection, wardrobe, item
from API.database import get_database, DB

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:4200",
]

app.include_router(collection.router, prefix="/collection", tags=["collection"])
app.include_router(item.router, prefix="/item", tags=["item"])
app.include_router(wardrobe.router, prefix="/wardrobe", tags=["wardrobe"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(ai_model.router, prefix="/ai", tags=["ai"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=random.random())

if __name__ == '__main__':
    conn = get_database()
    database = DB(conn)
    database.initialize_db()
    uvicorn.run("main:app", port=8000, log_level="info")
