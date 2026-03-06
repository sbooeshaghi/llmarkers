#!/usr/bin/env python3
from __future__ import annotations

import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

MODEL_NAME = 'sentence-transformers_all-MiniLM-L6-v2@float16'
MODEL_PATH = Path.home() / '.cache' / 'huggingface' / 'hub' / 'models--sentence-transformers--all-MiniLM-L6-v2' / 'snapshots' / 'c9745ed1d9f207416be6d2e6f8de32d1f16199bf'
EMBED_DTYPE = np.dtype('<f2')


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    db_path = repo_root / 'docs' / 'llmarkers.sqlite'
    if not db_path.exists():
        raise FileNotFoundError(db_path)
    if not MODEL_PATH.exists():
        raise FileNotFoundError(MODEL_PATH)

    with sqlite3.connect(db_path) as conn:
        profiles = pd.read_sql_query(
            '''
            SELECT profile_id, text_blob, paper_context_blob
            FROM profiles
            ORDER BY profile_id
            ''',
            conn,
        )

    model = SentenceTransformer(str(MODEL_PATH))
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
            MODEL_NAME,
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
        conn.execute('DELETE FROM profile_embeddings_biomed WHERE model_name = ?', (MODEL_NAME,))
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
            (MODEL_NAME,),
        ).fetchone()[0]

    print(f'Exported {exported:,} MiniLM profile embeddings to {db_path}.')


if __name__ == '__main__':
    main()
