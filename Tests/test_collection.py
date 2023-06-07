import os
import random
from unittest import TestCase

import requests
from sqlalchemy.ext.declarative import declarative_base

from API.database import DB, get_database
from Tests import helper_test

Base = declarative_base()
conn = get_database()
database = DB(conn)


class TestCollection(TestCase):
    def setUp(self):
        database.drop_db()
        database.initialize_db()
        helper_test.register_mock_user("test@test", "test")
        response = helper_test.login_mock_user("test@test", "test")
        self.token = response["token"]

    def test_collection_post_get_delete(self):
        directory = os.getcwd() + "/../Images/Assets/"
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
            for i in range(5):
                filename = random.choice(files)
                file_path = os.path.join(directory, folder, filename)

                with open(file_path, "rb") as image_file:
                    image_bytes = image_file.read()

                headers = {
                    "Authorization": "Bearer " + self.token,
                }

                data = {
                    "type": type,
                    "description": "item_description",
                    "tags": ["tag1", "tag2"],
                }

                file = {"image": (filename, image_bytes, "image/jpeg")}
                response = requests.post(url, data=data, files=file, headers=headers)

        url = "http://localhost:8000/collection/set"

        headers = {
            "Authorization": "Bearer " + self.token,
        }

        # post
        params = {"first_item_id": 1, "second_item_id": 2, "third_item_id": 3}

        response = requests.post(url, params=params, headers=headers)
        self.assertEqual(response.status_code, 200)

        # get
        set_id = response.json()["id"]
        url = f"http://localhost:8000/collection/sets/{set_id}"

        response = requests.get(url, headers=headers)
        self.assertEqual(response.status_code, 200)

        # delete
        response = requests.delete(url, headers=headers)
        self.assertEqual(response.status_code, 200)
