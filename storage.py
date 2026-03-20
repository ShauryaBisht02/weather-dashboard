import json
import os
from datetime import datetime

HISTORY_FILE = "history.json"

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as f:
        return json.load(f)

def save_to_history(city, weather_data):
    history = load_history()
    entry = {
        "city": city,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "temp": weather_data["temp"],
        "description": weather_data["description"]
    }
    if not history or history[-1]["city"].lower() != city.lower():
        history.append(entry)
    history = history[-10:]
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def clear_history():
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)