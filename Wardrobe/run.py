import json
import time

import requests

# import Wardrobe.led_controller as led

global_url = "http://localhost:8000"


def login_wardrobe(user_mail: str, serial_number: str):
    url = global_url + "/wardrobe/login_wardrobe"
    data = {
        "mail": user_mail,
        "password": serial_number,
    }
    response = requests.post(
        url, data=json.dumps(data), headers={"Content-Type": "application/json"}
    )
    return response


def download_all_clothes(token: str):
    url = global_url + "/collection/items/"
    headers = {
        "Authorization": "Bearer " + token,
    }
    response = requests.get(url, headers=headers)
    return response


def show_items_list(token: str):
    url = global_url + "/wardrobe/items"
    headers = {
        "Authorization": "Bearer " + token,
    }
    response = requests.get(url, headers=headers, timeout=60)
    return response


def parse_all_clothes(json_data):
    parsed_data = []
    for item in json_data:
        item_data = item["Item"]
        parsed_item = {
            "id": item_data["id"],
            "tags": item_data["tags"],
            "type": item_data["type"],
            "shelf": "",
            "position": "",
        }
        parsed_data.append(parsed_item)
    return parsed_data


if __name__ == "__main__":
    SERIAL_NUMBER = "77e9bb035caf2a1fbcb4992949660063bd430cec"
    user_mail = "test@test.com"

    token = None

    response = login_wardrobe(user_mail, SERIAL_NUMBER)
    while response.status_code != 200:
        response = login_wardrobe(user_mail, SERIAL_NUMBER)
        time.sleep(2)

    token = response.json()["token"]

    response = download_all_clothes(token)
    # json = parse_all_clothes(response.json())

    while True:
        response = show_items_list(token)
        # if response.status_code == 200:
        # led.on(response)
        # time.sleep(60)
