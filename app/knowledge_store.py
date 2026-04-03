import json
import os

STORE_PATH = "data/store.json"

def load_store():
    if not os.path.exists(STORE_PATH):
        return []

    with open(STORE_PATH, "r") as f:
        return json.load(f)

def add_document_entry(entry):
    data = load_store()
    data.append(entry)

    with open(STORE_PATH, "w") as f:
        json.dump(data, f, indent=2)