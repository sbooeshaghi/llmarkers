import pandas as pd
import json

def load_universal_labels_map():
    with open('../analysis/CELL_TYPE_KEYS.json') as f:
        cell_type_keys = sorted(json.load(f))
    return {i+1: value for i, value in enumerate(cell_type_keys)}

def load_evidence_labels(f):
    with open(f) as f:
        data = json.load(f)
    result = [obj['derived']['cell_type_label'] for obj in data]
    return result

def find_keys_with_same_value(d, value):
    return [k for k, v in d.items() if v == value]

def update_universal_labels():
    with open('../analysis/CELL_TYPE_KEYS.json', 'w') as f:
        json.dump(universal_labels.values(), f)

universal_labels = load_universal_labels_map()
folder_name = input("Folder name: ")
human_labels = load_evidence_labels(f'{folder_name}/evidence_human/evidence.json')
deg_labels = load_evidence_labels(f'{folder_name}/evidence_deg/evidence.json')

unique_hl = set(human_labels)
map_hl = {label: None for label in unique_hl}
unique_dl = set(deg_labels)
map_dl = {label: None for label in unique_dl}
og_size = len(universal_labels)

for label in unique_hl:
    print(universal_labels)
    print(label)
    ul = input("Universal label? Or N for none ")
    map_hl[label] = universal_labels[int(ul)] if ul != 'N' else label
    if ul == 'N':
        universal_labels[len(universal_labels) + 1] = label
    print(f"{int(ul)}/{len(universal_labels)}")

for label in unique_dl:
    print(universal_labels)
    print(label)
    ul = input("Universal label? Or N for none ")
    map_dl[label] = universal_labels[int(ul)] if ul != 'N' else label
    if ul == 'N':
        universal_labels[len(universal_labels) + 1] = label
    print(f"{int(ul)}/{len(universal_labels)}")

with open(f'{folder_name}/cell_mapping.json', 'w') as f:
    f.write("[")
    for label in universal_labels.values():
        result = []
        if label in map_hl.values():
            result.extend(find_keys_with_same_value(map_hl, label))
        if label in map_dl.values():
            result.extend(find_keys_with_same_value(map_dl, label))
        json.dump({label: result}, f, indent = 4)
        f.write(",\n")
    f.write("]")

update_universal_labels()

print("Done editing! Please check cell_map.json in your folder for the results and any updates in CELL_TYPE_KEYS.json")
