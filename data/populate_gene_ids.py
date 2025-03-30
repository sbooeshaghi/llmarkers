import json
import csv
import sys

def update_json_with_identifiers(json_path, tsv_path, output_path):
    # Step 1: Load the feature mapping, uppercasing keys
    feature_map = {}
    with open(tsv_path, 'r') as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            if len(row) >= 2:
                key = row[0].strip().upper()
                value = row[1].strip()
                feature_map[key] = value

    # Step 2: Load JSON
    with open(json_path, 'r') as f:
        data = json.load(f)

    # Step 3: Process and conditionally update
    for entry in data:
        derived = entry.get("derived", {})
        
        organism = derived.get("organism", "").strip().lower()
        if derived.get("feature_name", "") is str:
            feature_name = derived.get("feature_name", "").strip().upper()
        else:
            feature_name = derived.get("feature_name", "")
        if organism == "homo_sapiens" and feature_name in feature_map:
            derived["feature_identifier"] = feature_map[feature_name]
            derived["feature_identifier_type"] = "ensembl"

    # Step 4: Save updated JSON
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python update_json.py input.json mapping.tsv output.json")
        sys.exit(1)

    update_json_with_identifiers(sys.argv[1], sys.argv[2], sys.argv[3])
