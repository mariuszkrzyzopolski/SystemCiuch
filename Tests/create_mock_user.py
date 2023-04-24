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


def register_mock_user(mail, passwd):
    url = "http://localhost:8000/user/register"
    user_data = {
        "mail": mail,
        "city": "Gdansk",
        "password": passwd,
        "repeated_password": passwd,
    }
    response = requests.post(
        url, data=json.dumps(user_data), headers={"Content-Type": "application/json"}
    )
    return response


def login_mock_user(mail, passwd):
    url = "http://localhost:8000/user/login"
    user_data = {"mail": mail, "password": passwd}
    response = requests.post(
        url, data=json.dumps(user_data), headers={"Content-Type": "application/json"}
    )
    return response


def add_some_photos(token):
    directory = os.getcwd() + "/../Images/Assets/"
    folders = ["dress", "jumpsuit", "outwear", "pants", "shoes", "skirt", "top"]
    url = "http://localhost:8000/collection/item"

    for folder in folders:
        files = os.listdir(os.path.join(directory, folder))
        for i in range(5):
            filename = random.choice(files)
            file_path = os.path.join(directory, folder, filename)

            with open(file_path, "rb") as image_file:
                image_bytes = image_file.read()

            headers = {
                "Authorization": "Bearer " + token,
            }

            data = {
                "type": "item_type",
                "description": "item_description",
                "tags": ["tag1", "tag2"],
            }

            file = {"image": (filename, image_bytes, "image/jpeg")}
            response = requests.post(url, data=data, files=file, headers=headers)
    return response


if __name__ == "__main__":
    server = Process(target=run_server)
    server.start()
    time.sleep(1)

    for i in range(1,6):
        user = str(i) + "test@test.com"
        passwd = "password"
        response = register_mock_user(user, passwd)
        if response.status_code != 200:
            print(response.status_code, str(user) + " has not been registered")

        response = login_mock_user(user, passwd)
        token = response.json()["token"]
        if token is None:
            print(response.status_code, str(user) + " has not been logged in")

        response = add_some_photos(token)
        if response.status_code != 200:
            print(response.status_code, "Photos has not been added")

    src_file = "sql.db"
    dst_file = "../API/sql.db"

    abs_src = os.path.abspath(src_file)
    abs_dst = os.path.abspath(dst_file)

    shutil.copy(abs_src, abs_dst)
    print("DB has been changed")

    server.kill()
