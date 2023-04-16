import random
import time
import unittest
import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from multiprocessing import Process

from API import ai_model, collection, user, wardrobe
from API.database import DB, get_database
from Tests.test_user import TestUser

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
    "http://localhost:4200",
]

app.include_router(collection.router, tags=["collection"])
app.include_router(wardrobe.router, tags=["wardrobe"])
app.include_router(user.router, tags=["user"])
app.include_router(ai_model.router, tags=["ai"])
app.add_middleware(SessionMiddleware, secret_key=random.random())
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def run_server():
    conn = get_database()
    database = DB(conn)
    database.drop_db()
    database.initialize_db()
    uvicorn.run("test_app:app", port=8000, log_level="info")


if __name__ == "__main__":
    server = Process(target=run_server)
    server.start()
    time.sleep(1)

    suite = unittest.TestLoader().loadTestsFromTestCase(TestUser)
    unittest.TextTestRunner(verbosity=0).run(suite)

    server.kill()