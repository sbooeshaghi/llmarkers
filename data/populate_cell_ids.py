## IMPORTANT: THE CURRENT CELL MAPPINGS THAT EXIST ARE NOT POPULATED WITH EVIDENCE_LLM DATA

import json
import os

def find_key_given_value(label_map: dict, label):
    for key in label_map.keys():
        if label in label_map[key]:
            return key
    return None

def get_label_map(fn):
    with open(fn, 'r') as file:
        data = json.load(file)
        return data
    
def update_json(label_map, json_fn = 'evidence.json'):
    with open(json_fn, 'r') as file:
        data = json.load(file)
        
        for obj in data:
            obj['derived']['cell_type_id'] = find_key_given_value(label_map, obj['derived']['cell_type_label'])

        with open(json_fn, "w") as file:
            json.dump(data, file, indent = 4)

folder = input("Enter folder name: ")
deg_or_human = input("deg, human, or llm? ")

inner_folder = "evidence_human"
if deg_or_human == "deg":
    inner_folder = "evidence_deg"
elif deg_or_human == "llm":
    inner_folder = "evidence_llm"

fn = os.path.join(folder, inner_folder, "evidence.json")
label_map_fn = os.path.join(folder, "cell_mapping.json")
update_json(get_label_map(label_map_fn), fn)
print("Done!")