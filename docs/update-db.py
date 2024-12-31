# tool that takes in JSON evidence file and adds it to existing DuckDB database, creates new DuckDB database or creates a new one

import duckdb
import json
import pandas as pd

def load_citation(fn):
    with open(fn, 'r') as file:
        data = json.load(file)
    if 'citation' in list(data.keys()):
        return data['citation']
    return 'N/A'

def load_doi(fn):
    with open(fn, 'r') as file:
        data = json.load(file)
    if 'doi' in list(data.keys()):
        return data['doi']
    return 'N/A'

def load_evidence(fn):
    df = pd.read_json(fn)
    # Unwrap the 'source' column (contains a dictionary) into separate columns
    source_keys = ['source_type', 'source_rationale']
    derived_keys = ['organism', 'cell_source', 'cell_type_label', 'cell_state', 'gene', 'gene_id']
    source_df = df['source'].apply(lambda x: {k: x[k] for k in source_keys if k in x}).apply(pd.Series)
    derived_df = df['derived'].apply(lambda x: {k: x[k] for k in derived_keys if k in x}).apply(pd.Series)
    # Combine the original DataFrame with the unwrapped columns
    df = pd.concat([derived_df, source_df], axis=1)
    return df

def add_json_to_db(ev_file, db_file):
    evidence_df = load_evidence(f"../data/{ev_file}/evidence_human/evidence.json")
    citation = load_citation(f"../data/{ev_file}/citation.json")
    doi = load_doi(f"../data/{ev_file}/citation.json")

    evidence_df.insert(0, 'doi', doi)
    evidence_df.insert(1, 'citation', citation)
    
    conn = duckdb.connect(db_file) # connect to database
    table_name = 'evidence'
    #conn.execute(f'DROP TABLE IF EXISTS {table_name}') # FOR TESTING/DEBUGGING PURPOSES ONLY
    conn.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM evidence_df")
    conn.execute(f"INSERT INTO {table_name} SELECT * FROM evidence_df")
    
    result = conn.execute(f"SELECT * FROM {table_name}").fetchdf()
    print(result)
    conn.close()

evidence = input("Enter folder name of evidence: ")

add_json_to_db(evidence, "evidence.db")

