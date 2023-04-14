import json
import os
import random
import requests
import shutil
import time
import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from multiprocessing import Process

from API import ai_model, collection, user, wardrobe
from API.database import DB, get_database

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
    uvicorn.run("create_mock_user:app", port=8000, log_level="info")


def register_mock_user():
    url = "http://localhost:8000/user/register"
    user_data = {
        "mail": "test@test.com",
        "city": "Gdansk",
        "password": "password",
        "repeated_password": "password"
    }
    response = requests.post(url, data=json.dumps(user_data), headers={"Content-Type": "application/json"})
    return response.status_code


if __name__ == "__main__":
    server = Process(target=run_server)
    server.start()
    time.sleep(1)

    status = register_mock_user()
    if status == 200:
        print("User has been created")

    src_file = "sql.db"
    dst_file = "../API/sql.db"

    abs_src = os.path.abspath(src_file)
    abs_dst = os.path.abspath(dst_file)

    shutil.copy(abs_src, abs_dst)
    print("DB has been changed")

    server.kill()
