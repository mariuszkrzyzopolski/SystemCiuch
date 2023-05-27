import json

import pytest
import requests

pytestmark = pytest.mark.skip(reason="helper script")


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
    return response.json()


def login_mock_user(mail, passwd):
    url = "http://localhost:8000/user/login"
    user_data = {"mail": mail, "password": passwd}
    response = requests.post(
        url, data=json.dumps(user_data), headers={"Content-Type": "application/json"}
    )
    return response.json()
