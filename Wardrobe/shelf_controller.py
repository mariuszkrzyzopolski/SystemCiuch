import json

import led_controller as led

file_name = "shelf_db.json"
with open("wardrobe.config", "r") as file:
    wardrobe = json.load(file)


def add_item(id: int, shelf_number: int):
    with open(file_name, "r") as file:
        db = json.load(file)

    for shelf in db.values():
        if id in shelf:
            print("The item is already in the wardrobe.")
            return "Ok"
            break

    shelf = db.get(str(shelf_number), [])
    if len(shelf) < wardrobe[str(4)]["offset"]:
        shelf.append(id)
        db[str(shelf_number)] = shelf
        with open(file_name, "w") as file:
            json.dump(db, file)
        print("Item added successfully")
        return "Ok"
    else:
        return "Shelf overflow"


def remove_item(id: int):
    with open(file_name, "r") as file:
        db = json.load(file)

    removed = False
    for shelf_number, items in db.items():
        if id in items:
            items.remove(id)
            removed = True
            break

    if removed:
        with open(file_name, "w") as file:
            json.dump(db, file)
        print("Item removed successfully.")
    else:
        print("Item not found.")


def show_set(ids: [int]):
    cloth_dict = {}

    with open(file_name, "r") as file:
        db = json.load(file)

    for shelf_number, items in db.items():
        for index, item in enumerate(items):
            if item in ids:
                cloth_dict[item] = {"shelf": int(shelf_number), "position": index}
    cloth_dict = translate_position(cloth_dict)
    led.show_set(cloth_dict)
    return cloth_dict


def save_all(items_dict: {}):
    for item_id, item_type in items_dict.items():
        ret = None
        if "Upper garment" in item_type:
            ret = add_item(item_id, 1)
        elif item_type == "Lower garment":
            ret = add_item(item_id, 2)
        elif item_type == "Footwear":
            ret = add_item(item_id, 3)

        if ret == "Shelf overflow":
            ret = add_item(item_id, 4)
            if ret == "Shelf overflow":
                print("Wardrobe overflow")


def translate_position(cloth_set: dict):
    translated_position = []
    for item_id, item_info in cloth_set.items():
        shelf_number = str(item_info["shelf"])
        position = item_info["position"]
        LED_PIN = wardrobe[shelf_number]["LED_PIN"]
        offset = wardrobe[shelf_number]["offset"]
        new_position = wardrobe[shelf_number]["size"] + offset - position - 1
        translated_position.append({"LED_PIN": LED_PIN, "position": new_position})
    return translated_position


"""
if __name__ == "__main__":
    if not os.path.exists(file_name):
        if not os.path.exists(file_name):
            with open(file_name, "w") as file:
                json.dump({}, file)

    add_item(1, 2)
    add_item(2, 4)
    add_item(3, 1)
    print(show_set([1, 2, 3]))
    remove_item(3)
    print(show_set([1, 2, 3]))
"""
