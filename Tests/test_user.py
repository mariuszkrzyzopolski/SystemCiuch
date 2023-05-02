from unittest import TestCase
import requests
import json

from API.database import DB, get_database
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
conn = get_database()
database = DB(conn)


class TestUser(TestCase):
    def setUp(self):
        database.drop_db()
        database.initialize_db()

    def test_user_register(self):
        url = "http://localhost:8000/user/register"
        user_data = {
            "mail": "test@test.com",
            "city": "Gdansk",
            "password": "password",
            "repeated_password": "password",
        }

        response = requests.post(
            url,
            data=json.dumps(user_data),
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(response.status_code, 200)

    def test_register_second_user(self):
        url = "http://localhost:8000/user/register"
        user_data = {
            "mail": "test@test.com",
            "city": "Gdansk",
            "password": "password",
            "repeated_password": "password",
        }
        response = requests.post(
            url,
            data=json.dumps(user_data),
            headers={"Content-Type": "application/json"},
        )
        self.assertEqual(response.status_code, 200)
        response = requests.post(
            url,
            data=json.dumps(user_data),
            headers={"Content-Type": "application/json"},
        )
        self.assertNotEqual(response.status_code, 200)
