import json
import os

def update_map(path):
    with open(path, 'r') as f:
        data = json.loads(path)
    
    with open("CELL_TYPE_KEYS.json", 'r') as f:
        main_data = json.loads(f)
    
    for key, value in data.items():
        if key in main_data:
            main_data[key] = list(set(main_data[key]).union(set(value)))
        else:
            main_data[key] = list(set(value))
    
    with open("CELL_TYPE_KEYS.json") as f:
        json.dump(main_data, f, indent = 4)

def explore_folders():
    for dc in os.listdir("../data"):
        path = os.path.join("../data", dc, "cell_mapping.json")
        if os.path.exists(path):
            update_map(path)

explore_folders()
