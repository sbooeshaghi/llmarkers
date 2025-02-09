# tool that takes in JSON evidence file and adds it to existing DuckDB database, creates new DuckDB database or creates a new one

import duckdb
import json
import pandas as pd
import hashlib
import os
import uuid
import numpy as np

uuids = {}

def generate_hash(*args):
    combined_str = "_".join(str(arg) for arg in args if arg)
    return hashlib.sha256(combined_str.encode()).hexdigest()

def load_source_table(fn):
    df = pd.read_json(fn)

    organism_key = ['organism']
    organism_df = df['derived'].apply(lambda x: {k: x[k] for k in organism_key if k in x}).apply(pd.Series)

    source_keys = ['source_type', 'source_rationale']
    source_df = df['source'].apply(lambda x: {k: x[k] for k in source_keys if k in x}).apply(pd.Series)
   
    extracted_df = pd.DataFrame()
    extracted_df['extracted_id'] = [uuid.uuid4() for _ in range(len(organism_df))]

    derived_df = pd.DataFrame()
    derived_df['derived_id'] = [uuid.uuid4() for _ in range(len(organism_df))]

    df = pd.concat([extracted_df, derived_df, organism_df, source_df], axis=1)

    return df

def load_extracted_derived_table(fn, key, article_fn, source_df):
    result_df = pd.DataFrame() 
    result_df[key]= source_df[key]
    result_df['feature_id'] = [uuid.uuid4() for _ in range(len(result_df))]
    result_df['cell_id'] = [uuid.uuid4() for _ in range(len(result_df))]
    result_df['article_id'] = [uuid.uuid4() for _ in range(len(result_df))]

    return result_df

def load_cell_table(fn, extracted_df, derived_df):
    df = pd.read_json(fn)

    result_df = pd.DataFrame({'cell_id': pd.concat([extracted_df['cell_id'], derived_df['cell_id']], ignore_index=True)})

    cell_keys = ['cell_source', 'cell_state', 'cell_type_label']
    cell_derived_df = df['derived'].apply(lambda x: {k: x[k] for k in cell_keys if k in x}).apply(pd.Series)
    cell_extracted_df = df['extracted'].apply(lambda x: {k: x[k] for k in cell_keys if k in x}).apply(pd.Series)
    
    cell_df = pd.DataFrame({'cell_source': pd.concat([cell_derived_df['cell_source'], cell_extracted_df['cell_source']], ignore_index=True),
                            'cell_state': pd.concat([cell_derived_df['cell_state'], cell_extracted_df['cell_state']], ignore_index=True),
                            'cell_type_label': pd.concat([cell_derived_df['cell_type_label'], cell_extracted_df['cell_type_label']], ignore_index=True)})
    
    cell_type_ids = df['derived'].apply(lambda x: {k: x[k] for k in ['cell_type_id'] if k in x}).apply(pd.Series)

    cell_df['cell_type_id'] = cell_type_ids.astype(str)
    
    df = pd.concat([result_df, cell_df], axis=1)
    
    return df

def load_gene_table(fn, extracted_df, derived_df):
    df = pd.read_json(fn)

    result_df = pd.DataFrame({'feature_id': pd.concat([extracted_df['feature_id'], derived_df['feature_id']])})

    derived_genes = df['derived'].apply(lambda x: {k: x[k] for k in ['feature_name', 'feature_type'] if k in x}).apply(pd.Series)
    extracted_genes = df['extracted'].apply(lambda x: {k: x[k] for k in ['feature_name', 'feature_type'] if k in x}).apply(pd.Series)

    gene_df = pd.concat([derived_genes, extracted_genes])

    ensembl_ids = df['derived'].apply(lambda x: {k: x[k] for k in ['feature_identifier', 'feature_identifier_type'] if k in x}).apply(pd.Series)
    
    final_df = pd.concat([result_df, gene_df, ensembl_ids], axis = 1)
    
    return final_df

def load_article_table(fn, extracted_df, derived_df):
    result_df = pd.DataFrame({'article_id': pd.concat([extracted_df['article_id'], derived_df['article_id']], ignore_index=True)})
    
    citation = "none"
    doi = "none"

    if os.path.exists(fn):
        with open(fn) as f:
            citation_json = json.load(f)
        
        if 'citation' in citation_json.keys():
            citation = citation_json['citation']
        if 'doi' in citation_json.keys():
            doi = citation_json['doi']

    result_df['citation'], result_df['doi'] = citation, doi
    
    return result_df

def add_json_to_db(ev_file, h_or_d, db_file):
    conn = duckdb.connect(db_file) # connect to database
    """
    conn.execute(f'DROP TABLE IF EXISTS Source') # FOR TESTING/DEBUGGING PURPOSES ONLY
    conn.execute(f'DROP TABLE IF EXISTS Extracted') # FOR TESTING/DEBUGGING PURPOSES ONLY
    conn.execute(f'DROP TABLE IF EXISTS Derived') # FOR TESTING/DEBUGGING PURPOSES ONLY
    conn.execute(f'DROP TABLE IF EXISTS Cell') # FOR TESTING/DEBUGGING PURPOSES ONLY
    conn.execute(f'DROP TABLE IF EXISTS Gene') # FOR TESTING/DEBUGGING PURPOSES ONLY
    conn.execute(f'DROP TABLE IF EXISTS Article') # FOR TESTING/DEBUGGING PURPOSES ONLY
    """
    folder_name = "evidence_human"

    if h_or_d == 'd':
        folder_name = "evidence_deg"
    
    # source_df
    source_df = load_source_table(f"../data/{ev_file}/{folder_name}/evidence.json")
    #conn.execute(f"CREATE TABLE IF NOT EXISTS Source AS SELECT * FROM source_df")
    conn.execute(f"INSERT INTO Source SELECT * FROM source_df")
    
    # extracted_df
    extracted_df = load_extracted_derived_table(f"../data/{ev_file}/{folder_name}/evidence.json", "extracted_id", f"../data/{ev_file}/citation.json", source_df)
    #conn.execute(f"CREATE TABLE IF NOT EXISTS Extracted AS SELECT * FROM extracted_df")
    conn.execute(f"INSERT INTO Extracted SELECT * FROM extracted_df")

    # derived_df
    derived_df = load_extracted_derived_table(f"../data/{ev_file}/{folder_name}/evidence.json", "derived_id", f"../data/{ev_file}/citation.json", source_df)
    #conn.execute(f"CREATE TABLE IF NOT EXISTS Derived AS SELECT * FROM derived_df")
    conn.execute(f"INSERT INTO Derived SELECT * FROM derived_df")
   
    # cell_df
    cell_df = load_cell_table(f"../data/{ev_file}/{folder_name}/evidence.json", extracted_df, derived_df)
    #conn.execute(f"CREATE TABLE IF NOT EXISTS Cell AS SELECT * FROM cell_df")
    conn.execute(f"INSERT INTO Cell SELECT * FROM cell_df")

    # gene_df
    gene_df = load_gene_table(f"../data/{ev_file}/{folder_name}/evidence.json", extracted_df, derived_df)
    #conn.execute(f"CREATE TABLE IF NOT EXISTS Gene AS SELECT * FROM gene_df")
    conn.execute(f"INSERT INTO Gene SELECT * FROM gene_df")

    # article_df
    article_df = load_article_table(f"../data/{ev_file}/citation.json", extracted_df, derived_df)
    #conn.execute(f"CREATE TABLE IF NOT EXISTS Article AS SELECT * FROM article_df")
    conn.execute(f"INSERT INTO Article SELECT * FROM article_df")
    
    conn.close()

    print("Done!")

evidence = input("Enter folder name of evidence: ")
human_or_deg = input("Human (h) or DEG (d)? ")

add_json_to_db(evidence, human_or_deg, "evidence.db")

