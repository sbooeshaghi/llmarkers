#!/usr/bin/env python3
import json
import os
import argparse
from typing import Dict, List


def load_universal_labels_map(keys_path: str) -> Dict[int, str]:
    """Load cell type keys from a JSON file and create a numbered mapping."""
    try:
        with open(keys_path) as f:
            cell_type_keys = sorted([key.strip().upper() for key in json.load(f)])
        return {i + 1: value for i, value in enumerate(cell_type_keys)}
    except FileNotFoundError:
        print(f"Warning: Cell type keys file not found at {keys_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Warning: Invalid JSON in cell type keys file at {keys_path}")
        return {}


def load_evidence_labels(filepath: str, universal_map) -> List[str]:
    """Load cell type labels from an evidence JSON file."""
    try:
        with open(filepath) as f:
            data = json.load(f)
        return [obj['derived']['cell_type_label'].strip().upper() for obj in data if obj['derived']['cell_type_id'] is None or obj['derived']['cell_type_id'] not in universal_map.values()]
    except FileNotFoundError:
        print(f"Warning: Evidence file not found at {filepath}")
        return []
    except (json.JSONDecodeError, KeyError) as e:
        print(f"Warning: Error parsing evidence file at {filepath}: {e}")
        return []


def find_keys_with_same_value(d: Dict, value: str) -> List[str]:
    """Find all keys in a dictionary that have a specific value."""
    return [k for k, v in d.items() if v == value]


def ensure_directory_exists(path: str) -> None:
    """Create directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)


def main():
    parser = argparse.ArgumentParser(description='Create cell type mapping')
    parser.add_argument('--human', help='Path to the human evidence JSON file')
    parser.add_argument('--deg', help='Path to the DEG evidence JSON file')
    parser.add_argument('--llm', help='Path to the LLM evidence JSON file')
    parser.add_argument('-o', '--output', required=True, help='Output directory for the mapping files')
    parser.add_argument('-k', '--keys', help='Path to the cell type keys file', default='../analysis/CELL_TYPE_KEYS.json')
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    ensure_directory_exists(args.output)
    
    # Load universal labels
    universal_labels = load_universal_labels_map(args.keys)
    
    # Load evidence labels for each specified path
    all_labels: List[str] = []
    
    if args.human:
        human_labels = load_evidence_labels(args.human, universal_labels)
        all_labels.extend(human_labels)
        print(f"Loaded {len(human_labels)} human evidence labels from {args.human}")
    
    if args.deg:
        deg_labels = load_evidence_labels(args.deg, universal_labels)
        all_labels.extend(deg_labels)
        print(f"Loaded {len(deg_labels)} DEG evidence labels from {args.deg}")
    
    if args.llm:
        llm_labels = load_evidence_labels(args.llm, universal_labels)
        all_labels.extend(llm_labels)
        print(f"Loaded {len(llm_labels)} LLM evidence labels from {args.llm}")
    
    if not all_labels:
        #print("Error: No evidence files provided. Please specify at least one evidence file with --human, --deg, or --llm")
        return
    
    # Get unique labels
    unique_labels = set(all_labels)
    print(f"Found {len(unique_labels)} unique cell type labels")
    
    # Create mapping
    combined_map = {label: None for label in unique_labels}
    
    for idx, label in enumerate(unique_labels):
        print(f"\n{idx + 1}/{len(unique_labels)}")
        print("Available universal labels:")
        for ul_id, ul_label in universal_labels.items():
            print(f"{ul_id}: {ul_label}")
        
        print(f"\nCurrent label: {label}")
        
        while True:
            ul = input("Universal label number? (or 'N' for new label) ")
            if ul.upper() == 'N':
                combined_map[label] = label.upper().strip()
                next_id = max(universal_labels.keys()) + 1 if universal_labels else 1
                universal_labels[next_id] = label
                break
            try:
                ul_int = int(ul)
                if ul_int in universal_labels:
                    combined_map[label] = universal_labels[ul_int]
                    break
                else:
                    print(f"Invalid label number. Please choose from {list(universal_labels.keys())} or 'N'")
            except ValueError:
                print("Please enter a valid number or 'N'")
    
    # Create final mapping
    final_map = {}
    for label in universal_labels.values():
        result = find_keys_with_same_value(combined_map, label)
        if result:
            final_map[label] = result
    
    # Save output files
    with open(f'{args.output}/ctmap.json', 'w') as f:
        json.dump(final_map, f, indent=4)
        print(f"Saved mapping to {args.output}/ctmap.json")
    
    with open(f'{args.output}/rev_ctmap.json', 'w') as f:
        json.dump(combined_map, f, indent=4)
        print(f"Saved reverse mapping to {args.output}/rev_ctmap.json")
    
    # Update cell type keys if needed
    with open(args.keys, 'w') as f:
        json.dump(list(universal_labels.values()), f, indent=4)
        print(f"Updated cell type keys at {args.keys}")
    
    print("\nDone! Cell type mapping complete.")

if __name__ == "__main__":
    main()