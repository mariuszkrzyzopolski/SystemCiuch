import json
import os
import time

import requests
import shelf_controller as shelf
from requests.exceptions import ConnectionError

global_url = "http://localhost:8000"
sleep = 5


def login_wardrobe(user_mail: str, serial_number: str):
    url = global_url + "/wardrobe/login_wardrobe"
    data = {
        "mail": user_mail,
        "password": serial_number,
    }

    try:
        response = requests.post(
            url, data=json.dumps(data), headers={"Content-Type": "application/json"}
        )
        return response
    except ConnectionError as e:
        print("Connection error:", str(e))
        return None


def download_all_clothes(token: str):
    url = global_url + "/collection/items/"
    headers = {
        "Authorization": "Bearer " + token,
    }
    try:
        response = requests.get(url, headers=headers, timeout=60)
        return response
    except ConnectionError as e:
        print("Connection error:", str(e))
        return None


def to_highlight(token: str):
    url = global_url + "/wardrobe/get_command"
    headers = {
        "Authorization": "Bearer " + token,
    }
    try:
        response = requests.get(url, headers=headers, timeout=60)
        return response
    except ConnectionError as e:
        print("Connection error:", str(e))
        return None


def items_parser(items_list: []):
    items_dict = {}
    for item in items_list:
        items_dict[item["Item"]["id"]] = item["Item"]["type"]
    return items_dict


if __name__ == "__main__":
    SERIAL_NUMBER = "77e9bb035caf2a1fbcb4992949660063bd430cec"
    user_mail = "test@test.com"

    token = ""
    logged_in = False

    if not os.path.exists(shelf.file_name):
        with open(shelf.file_name, "w") as file:
            json.dump({}, file)
    while True:
        if not logged_in:
            response = login_wardrobe(user_mail, SERIAL_NUMBER)
            if response is None or response.status_code != 200:
                if response == -1:
                    print("Server is not running")
                else:
                    print("Something went wrong with login")
                logged_in = False
                time.sleep(sleep)
            else:
                token = response.json().get("token", "")
                logged_in = True
        else:
            response = download_all_clothes(token)
            if response is not None and response.status_code == 200:
                commands = response.json()
                if isinstance(commands, list) and len(commands) > 0:
                    items_dict = items_parser(commands)
                    shelf.save_all(items_dict)
                break
            else:
                print("Something went wrong with get_command")

    while True:
        if not logged_in:
            response = login_wardrobe(user_mail, SERIAL_NUMBER)
            if response is None or response.status_code != 200:
                if response == -1:
                    print("Server is not running")
                else:
                    print("Something went wrong with login")
                logged_in = False
                time.sleep(sleep)
            else:
                token = response.json().get("token", "")
                logged_in = True

        else:
            response = to_highlight(token)
            if response is not None and response.status_code == 200:
                commands = response.json()
                print(commands)
                if isinstance(commands, list) and len(commands) > 0:
                    shelf.show_set(commands)
            else:
                print("Something went wrong with get_command")

        time.sleep(sleep)
