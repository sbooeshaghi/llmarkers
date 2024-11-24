# given two JSON files, we want to compare the genes if cell_type is same and cell_type if genes are same
import json

file1 = 'evidence_emont.json'
file2 = 'evidence_vijay.json'

with open(file1, 'r') as f1, open(file2, 'r') as f2:
    data1 = json.load(f1)
    data2 = json.load(f2)


for item1 in data1:
    for item2 in data2:
        if item1['cell_type'] == item2['cell_type'] or item1['gene'] == item2['gene']:
            with open("similarities.txt", "a") as file:
                file.write("Similarity Found\n")
                file.write(json.dumps(item1))
                file.write("\n")
                file.write(json.dumps(item2))
                file.write("\n\n")