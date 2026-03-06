#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


def fmt_mb(n_bytes: float) -> str:
    return f"{n_bytes / 1e6:,.1f} MB"


def scalar(conn: sqlite3.Connection, query: str) -> int:
    row = conn.execute(query).fetchone()
    return int(row[0]) if row and row[0] is not None else 0


def main() -> None:
    parser = argparse.ArgumentParser(description="Estimate browser deployment size for a biomedical embedding model.")
    parser.add_argument(
        "--db",
        type=Path,
        default=Path("docs/llmarkers.sqlite"),
        help="Path to the LLMarkers SQLite database.",
    )
    parser.add_argument(
        "--model-dir",
        type=Path,
        default=Path.home() / ".cache" / "torch" / "sentence_transformers" / "pritamdeka_BioBERT-mnli-snli-scinli-scitail-mednli-stsb",
        help="Path to the cached sentence-transformer model directory.",
    )
    parser.add_argument("--dim", type=int, default=768, help="Embedding dimension.")
    parser.add_argument("--fields", type=int, default=2, help="Number of embedding fields stored per profile.")
    args = parser.parse_args()

    if not args.db.exists():
        raise FileNotFoundError(f"Missing SQLite database: {args.db}")
    if not args.model_dir.exists():
        raise FileNotFoundError(f"Missing model directory: {args.model_dir}")

    with sqlite3.connect(args.db) as conn:
        n_profiles = scalar(conn, "SELECT COUNT(*) FROM profiles")

    total_model_bytes = sum(path.stat().st_size for path in args.model_dir.rglob("*") if path.is_file())
    pytorch_bin = args.model_dir / "pytorch_model.bin"
    pytorch_bytes = pytorch_bin.stat().st_size if pytorch_bin.exists() else total_model_bytes

    float32_embed_bytes = n_profiles * args.dim * args.fields * 4
    float16_embed_bytes = n_profiles * args.dim * args.fields * 2
    int8_embed_bytes = n_profiles * args.dim * args.fields

    print("Biomedical browser deployment estimate")
    print(f"Database:        {args.db}")
    print(f"Model dir:       {args.model_dir}")
    print(f"Profiles:        {n_profiles:,}")
    print(f"Embedding dim:   {args.dim}")
    print(f"Embedding fields per profile: {args.fields}")
    print()
    print("Model artifact")
    print(f"  Current cached model dir:   {fmt_mb(total_model_bytes)}")
    print(f"  Current pytorch_model.bin:  {fmt_mb(pytorch_bytes)}")
    print(f"  Rough fp16 equivalent:      {fmt_mb(pytorch_bytes / 2)}")
    print(f"  Rough int8 equivalent:      {fmt_mb(pytorch_bytes / 4)}")
    print()
    print("Profile embedding payload")
    print(f"  float32 binary:             {fmt_mb(float32_embed_bytes)}")
    print(f"  float16 binary:             {fmt_mb(float16_embed_bytes)}")
    print(f"  int8 binary:                {fmt_mb(int8_embed_bytes)}")
    print()
    print("Practical reading")
    print("  - Storing profile vectors in SQLite is feasible.")
    print("  - The hard part is shipping a browser-compatible query encoder.")
    print("  - A 400+ MB PyTorch checkpoint is too heavy for a practical static site.")
    print("  - A smaller ONNX/WebGPU model or a different lightweight embedding model is more realistic.")


if __name__ == "__main__":
    main()
