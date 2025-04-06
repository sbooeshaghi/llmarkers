#!/usr/bin/env python3

import argparse
import json
import os
import re

def split_text_into_windows(corpus, window_size=500, overlap=250, document_name="doc"):
    corpus = re.sub(r'\n+', ' ', corpus.strip())
    results = []
    step_size = window_size - overlap

    for start_idx in range(0, len(corpus), step_size):
        end_idx = min(start_idx + window_size, len(corpus))

        extracted_text = corpus[start_idx:end_idx]

        results.append({
            "extracted_text": extracted_text,
            "start_idx": start_idx,
            "end_idx": end_idx,
            "index_type": "character",
            "document_name": document_name
        })

        if end_idx == len(corpus):
            break

    return results


def main():
    parser = argparse.ArgumentParser(description="Split text into fixed-size windows with overlap.")
    parser.add_argument("--corpus", required=True, help="Path to text corpus file")
    parser.add_argument("--window_size", type=int, default=500, help="Size of each text window in characters")
    parser.add_argument("--overlap", type=int, default=250, help="Overlap between consecutive windows in characters")
    parser.add_argument("--output", required=True, help="Output JSON file path")

    args = parser.parse_args()

    if not os.path.exists(args.corpus):
        raise FileNotFoundError("Corpus file not found.")

    with open(args.corpus, 'r', encoding='utf-8') as f:
        corpus = f.read()

    document_name = os.path.basename(args.corpus)

    extracted_results = split_text_into_windows(
        corpus, window_size=args.window_size, overlap=args.overlap, document_name=document_name
    )

    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(extracted_results, f, indent=2)

    print(f"Text splitting completed. Results saved to '{args.output}'")


if __name__ == "__main__":
    main()

