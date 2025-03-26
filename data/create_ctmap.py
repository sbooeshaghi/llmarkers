import json
import os

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

universal_labels = load_universal_labels_map()
folder_name = input("Folder name: ")
include_degs = input("Include degs? (y or n) ")
include_llm = input("Include LLM evidence? (y or n) ")
human_labels = load_evidence_labels(f'{folder_name}/evidence_human/evidence.json')
deg_labels = set()
if include_degs != "n":
    deg_labels = load_evidence_labels(f'{folder_name}/evidence_deg/evidence.json')
llm_labels = set()
if include_llm != "n":
    model_name = input("Model used for LLM evidence: ")
    llm_labels = load_evidence_labels(f'{folder_name}/evidence_llm_{model_name}/evidence.json')

unique_hl = set(human_labels)
unique_dl = set(deg_labels)
unique_llm = set(llm_labels)
combined = set(unique_hl.union(unique_dl))
combined = set(combined.union(unique_llm))
combined_map = {label: None for label in combined}

for idx, label in enumerate(combined):
    print(f"\n{idx + 1}/{len(combined)}\n")
    print(universal_labels)
    print(f"\n{label}\n")
    ul = input("Universal label? Or N for none ")
    combined_map[label] = universal_labels[int(ul)] if ul != 'N' else label
    if ul == 'N':
        universal_labels[len(universal_labels) + 1] = label

final_map = {}
for idx, label in enumerate(universal_labels.values()):
    result = []
    result.extend(find_keys_with_same_value(combined_map, label))
    if result != []:
        final_map[label] = result  

data = json.dumps(final_map)
path = f'{folder_name}/ctmap'

if not os.path.exists(path):
    os.mkdir(path)

with open(f'{path}/ctmap.json', 'w') as f:
    json.dump(final_map, f, indent = 4)

with open(f'{path}/rev_ctmap.json', 'w') as f:
    json.dump(combined_map, f, indent = 4)

with open('../analysis/CELL_TYPE_KEYS.json', 'w') as f:
    json.dump(list(universal_labels.values()), f, indent = 4)

print("Done editing! Please check ctmap.json in your folder for the results and any updates in CELL_TYPE_KEYS.json\n")
