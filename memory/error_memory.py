import json
import os

DB_FILE = "memory/fix_database.json"


def load_memory():
    if not os.path.exists(DB_FILE):
        return {}

    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_memory(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)


def get_fix(error):

    data = load_memory()

    for key in data:
        if key in error:
            return data[key]

    return None


def store_fix(error, fix):

    data = load_memory()

    data[error] = fix

    save_memory(data)