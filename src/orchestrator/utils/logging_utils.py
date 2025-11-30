import json

def save_log(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
