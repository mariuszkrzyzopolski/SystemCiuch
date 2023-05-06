import os
from unittest import TestCase
import requests
import helper_test
import random

from API.database import DB, get_database
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
conn = get_database()
database = DB(conn)


class TestItem(TestCase):
    def setUp(self):
        database.drop_db()
        database.initialize_db()
        helper_test.register_mock_user("test@test", "test")
        response = helper_test.login_mock_user("test@test", "test")
        self.token = response["token"]

    def test_item_post(self):
        url = "http://localhost:8000/collection/item"

        directory = os.getcwd() + "/../Images/Assets/"
        folders = ["dress", "jumpsuit", "outwear", "pants", "shoes", "skirt", "top"]

        for folder in folders:
            files = os.listdir(os.path.join(directory, folder))
            filename = random.choice(files)
            file_path = os.path.join(directory, folder, filename)

        with open(file_path, "rb") as image_file:
            image_bytes = image_file.read()

        headers = {
            "Authorization": "Bearer " + self.token,
        }

        data = {
            "type": "top",
            "description": "item_description",
            "tags": ["tag1", "tag2"],
        }

        file = {"image": (filename, image_bytes, "image/jpeg")}
        response = requests.post(url, data=data, files=file, headers=headers)
        self.assertEqual(response.status_code, 200)