import json
import os
from datetime import datetime

DATA_FILE = "progress_data.json"

def load_progress():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_attempt(module, details):
    data = load_progress()
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "module": module,
        "details": details
    }
    data.append(entry)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_module_history(module):
    data = load_progress()
    return [entry for entry in data if entry["module"] == module]