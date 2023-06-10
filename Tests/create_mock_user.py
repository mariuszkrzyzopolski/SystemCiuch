import json
import os
import random
import shutil
import time
from multiprocessing import Process

import pytest
import requests
import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from API import collection, user, wardrobe
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


@pytest.mark.skip(reason="helper function")
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


@pytest.mark.skip(reason="helper function")
def login_mock_user(mail, passwd):
    url = "http://localhost:8000/user/login"
    user_data = {"mail": mail, "password": passwd}
    response = requests.post(
        url, data=json.dumps(user_data), headers={"Content-Type": "application/json"}
    )
    return response


@pytest.mark.skip(reason="helper function")
def register_wardrobe(wardrobe_code, token):
    url = "http://localhost:8000/wardrobe/connect"
    data = {
        "wardrobe_code": wardrobe_code,
    }
    headers = {
        "Authorization": "Bearer " + token,
    }
    response = requests.post(url, data=json.dumps(data), headers=headers)
    return response


@pytest.mark.skip(reason="helper function")
def add_some_photos(token):
    directory = os.getcwd() + "/Images/Assets/"
    folders = ["dress", "jumpsuit", "outwear", "pants", "shoes", "skirt", "top"]
    url = "http://localhost:8000/collection/item"

    for folder in folders:
        files = os.listdir(os.path.join(directory, folder))
        if folder in ["dress", "jumpsuit", "outwear", "top"]:
            type = "Upper garment"
        elif folder in ["pants", "skirt"]:
            type = "Lower garment"
        elif folder in ["shoes"]:
            type = "Footwear"
        tags = folder
        for i in range(5):
            filename = random.choice(files)
            file_path = os.path.join(directory, folder, filename)

            with open(file_path, "rb") as image_file:
                image_bytes = image_file.read()

            headers = {
                "Authorization": "Bearer " + token,
            }

            data = {
                "type": type,
                "description": "item_description",
                "tags": [tags],
            }

            file = {"image": (filename, image_bytes, "image/jpeg")}
            response = requests.post(url, data=data, files=file, headers=headers)
    return response


if __name__ == "__main__":
    server = Process(target=run_server)
    server.start()
    time.sleep(20)

    user = "test@test.com"
    passwd = "password"
    response = register_mock_user(user, passwd)
    if response.status_code != 200:
        print(response.status_code, str(user) + " has not been registered")

    response = login_mock_user(user, passwd)
    token = response.json()["token"]
    if token is None:
        print(response.status_code, str(user) + " has not been logged in")

    response = register_wardrobe("77e9bb035caf2a1fbcb4992949660063bd430cec", token)
    if response.status_code != 200:
        print(response.status_code, "Wardrobe has not been added")

    response = add_some_photos(token)
    if response.status_code != 200:
        print(response.status_code, "Photos has not been added")

    src_file = "sql.db"
    dst_file = "API/sql.db"

    abs_src = os.path.abspath(src_file)
    abs_dst = os.path.abspath(dst_file)

    shutil.copy(abs_src, abs_dst)
    print("DB has been changed")

    server.kill()
