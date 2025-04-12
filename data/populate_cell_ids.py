import json
import os

def find_key_given_value(label_map: dict, label):
    
    for key in label_map.keys():
        if label in label_map[key]:
            return key
        else:
            print(label_map[key], label)
    return None

def get_label_map(fn):
    with open(fn, 'r') as file:
        data = json.load(file)
        return data
    
def update_json(label_map, json_fn = 'evidence.json'):
    with open(json_fn, 'r') as file:
        data = json.load(file)
        
        for obj in data:
            if obj['derived']['cell_type_label'] is not None:
                obj['derived']['cell_type_id'] = find_key_given_value(label_map, obj['derived']['cell_type_label'].upper().strip())
            #print(label_map[obj['derived']['cell_type_label'].upper()])
            #obj['derived']['cell_type_id'] = label_map[obj['derived']['cell_type_label'].upper().strip()]
        with open(json_fn, "w") as file:
            json.dump(data, file, indent = 4)

# user functionality: 
folder = input("Enter folder name: ")
deg_or_human = ""

while deg_or_human != "done":
    deg_or_human = input("deg, human, or llm? type \"done\" if done editing: ")
    inner_folder = "evidence_human"
    ev_fn = "evidence.json"
    if deg_or_human == "deg":
        inner_folder = "evidence_deg"
        f_or_uf = input("filtered or unfiltered? (f / u): ")
        if f_or_uf == 'u':
            ev_fn = "evidence_unfiltered.json"
    elif deg_or_human == "llm":
        inner_folder = f"evidence_llm_llama3.2_MarkerGeneListStrict_4efcc22"

    fn = os.path.join(folder, inner_folder, ev_fn)
    label_map_fn = os.path.join(folder, "ctmap", "ctmap.json")
    update_json(get_label_map(label_map_fn), fn)
    print("Finished editing", inner_folder, "\n")

print("Done!")