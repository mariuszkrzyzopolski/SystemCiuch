import json
import os
import random
import shutil
import time
from multiprocessing import Process

import requests
import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

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
        "repeated_password": "password",
    }
    response = requests.post(
        url, data=json.dumps(user_data), headers={"Content-Type": "application/json"}
    )
    return response.status_code


def add_some_photos():
    directory = os.getcwd()
    filename = "19861371.jpg"
    file_path = directory + "/../Images/Assets/dress/" + filename

    url = "http://localhost:8000/user/login"
    user_data = {"mail": "test@test.com", "password": "password"}
    response = requests.post(
        url, data=json.dumps(user_data), headers={"Content-Type": "application/json"}
    )
    token = response.json()["token"]

    url = "http://localhost:8000/collection/item"

    with open(file_path, "rb") as image_file:
        image_bytes = image_file.read()

    headers = {
        "Authorization": "Bearer " + token,
        # "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
    }

    data = {
        "type": "item_type",
        "description": "item_description",
        "tags": ["tag1", "tag2"],
        # "image": im_b64
    }

    files = {"image": ("image.jpg", image_bytes, "image/jpeg")}

    response = requests.post(url, data=data, files=files, headers=headers)
    print(response.text)
    return response.status_code


if __name__ == "__main__":
    server = Process(target=run_server)
    server.start()
    time.sleep(1)

    status = register_mock_user()
    if status == 200:
        print("User has been created")
    status = add_some_photos()
    if status == 200:
        print("Photos added")
    print(status)

    src_file = "sql.db"
    dst_file = "../API/sql.db"

    abs_src = os.path.abspath(src_file)
    abs_dst = os.path.abspath(dst_file)

    shutil.copy(abs_src, abs_dst)
    print("DB has been changed")

    server.kill()
