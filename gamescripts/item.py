#gamescripts/item.py
import os
import json

class Item:
    def __init__(self, id_, name, type_, description, value=0, **kwargs):
        self.id = id_
        self.name = name
        self.type = type_
        self.description = description
        self.value = value
        self.attributes = kwargs

    def __repr__(self):
        return f"<Item: {self.name} ({self.type})>"

def load_items_from_json(file_path="gamedata/resources/items/items.json"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"No item file at {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        item_data_list = json.load(f)

    loaded_items = {}
    for data in item_data_list:
        item = Item(
            id_=data["id"],
            name=data["name"],
            type_=data["type"],
            description=data["description"],
            value=data.get("value", 0),
            **{k: v for k, v in data.items() if k not in ["id", "name", "type", "description", "value"]}
        )
        loaded_items[item] = item

    return loaded_items

ITEMS = load_items_from_json()
