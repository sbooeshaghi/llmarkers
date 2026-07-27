#!/usr/bin/env python3
"""Legacy MiniLM exporter retained for the archived pre-.onto website."""

from __future__ import annotations

import argparse
import os
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

DEFAULT_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'
DEFAULT_MODEL_REVISION = os.environ.get('LLMARKERS_MINILM_MODEL_REVISION')
EMBED_DTYPE = np.dtype('<f2')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Export MiniLM profile embeddings into docs/llmarkers.sqlite.')
    parser.add_argument(
        '--model',
        default=os.environ.get('LLMARKERS_MINILM_MODEL', DEFAULT_MODEL),
        help='SentenceTransformer model ID or local model path. Defaults to %(default)s.',
    )
    parser.add_argument(
        '--model-name',
        default=None,
        help='Model name stored in SQLite. Defaults to a normalized --model value plus @float16.',
    )
    parser.add_argument(
        '--model-revision',
        default=DEFAULT_MODEL_REVISION,
        help='Optional Hugging Face revision for --model. Also included in the stored model name.',
    )
    parser.add_argument(
        '--db',
        type=Path,
        default=None,
        help='SQLite database path. Defaults to docs/llmarkers.sqlite.',
    )
    return parser.parse_args()


def stored_model_name(model: str, override: str | None, revision: str | None) -> str:
    if override:
        return override
    model_path = Path(model)
    if model_path.exists():
        name = model_path.name
    else:
        name = model.replace('/', '_')
    if revision:
        return f'{name}@{revision}@float16'
    return f'{name}@float16'


def main() -> None:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    db_path = args.db or repo_root / 'docs' / 'llmarkers.sqlite'
    if not db_path.exists():
        raise FileNotFoundError(db_path)
    model_name = stored_model_name(args.model, args.model_name, args.model_revision)

    with sqlite3.connect(db_path) as conn:
        profiles = pd.read_sql_query(
            '''
            SELECT profile_id, text_blob, paper_context_blob
            FROM profiles
            ORDER BY profile_id
            ''',
            conn,
        )

    if args.model_revision:
        model = SentenceTransformer(args.model, revision=args.model_revision)
    else:
        model = SentenceTransformer(args.model)
    text_embeddings = model.encode(
        profiles['text_blob'].fillna('').tolist(),
        normalize_embeddings=True,
        show_progress_bar=True,
    )
    context_embeddings = model.encode(
        profiles['paper_context_blob'].fillna('').tolist(),
        normalize_embeddings=True,
        show_progress_bar=True,
    )
    dim = int(text_embeddings.shape[1])

    records = [
        (
            int(profile_id),
            model_name,
            dim,
            'float16',
            np.asarray(text_vec, dtype=EMBED_DTYPE).tobytes(),
            np.asarray(context_vec, dtype=EMBED_DTYPE).tobytes(),
        )
        for profile_id, text_vec, context_vec in zip(profiles['profile_id'], text_embeddings, context_embeddings)
    ]

    with sqlite3.connect(db_path) as conn:
        conn.execute('PRAGMA foreign_keys = ON')
        conn.execute(
            '''
            CREATE TABLE IF NOT EXISTS profile_embeddings_biomed (
                profile_id INTEGER NOT NULL REFERENCES profiles(profile_id),
                model_name TEXT NOT NULL,
                dim INTEGER NOT NULL,
                dtype TEXT NOT NULL,
                text_embedding_blob BLOB NOT NULL,
                context_embedding_blob BLOB NOT NULL,
                PRIMARY KEY (profile_id, model_name)
            )
            '''
        )
        conn.execute('DELETE FROM profile_embeddings_biomed WHERE model_name = ?', (model_name,))
        conn.executemany(
            '''
            INSERT INTO profile_embeddings_biomed (
                profile_id,
                model_name,
                dim,
                dtype,
                text_embedding_blob,
                context_embedding_blob
            ) VALUES (?, ?, ?, ?, ?, ?)
            ''',
            records,
        )
        conn.commit()
        exported = conn.execute(
            'SELECT COUNT(*) FROM profile_embeddings_biomed WHERE model_name = ?',
            (model_name,),
        ).fetchone()[0]

    print(f'Exported {exported:,} MiniLM profile embeddings to {db_path} using {model_name}.')


if __name__ == '__main__':
    main()
