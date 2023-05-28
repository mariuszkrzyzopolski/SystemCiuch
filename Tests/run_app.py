import random
import time
import unittest

import pytest
import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from multiprocessing import Process

from API import collection, user, wardrobe
from API.database import DB, get_database
from Tests.test_user import TestUser
from Tests.test_item import TestItem
from Tests.test_collection import TestCollection

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
app.add_middleware(SessionMiddleware, secret_key=random.random())
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@pytest.mark.skip(reason="helper")
def run_server():
    conn = get_database()
    database = DB(conn)
    database.drop_db()
    database.initialize_db()
    uvicorn.run("test_app:app", port=8000, log_level="info")


if __name__ == "__main__":
    run_server()
    """
    server = Process(target=run_server)
    server.start()
    time.sleep(3)

    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUser))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestItem))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestCollection))
    unittest.TextTestRunner(verbosity=0).run(suite)

    server.kill()
    """