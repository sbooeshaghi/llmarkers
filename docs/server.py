# pip install duckdb

import duckdb
rel = duckdb.read_json("evidence.json") # returns a relation
# rel.show() # we can see the relation

# we can query certain Python variables by referring to their variable name using DuckDB relations 

def get_all_genes():
    genes = duckdb.sql("SELECT extracted.gene FROM rel").fetchall()
    return set(genes) # to make sure theyre not repeated

def get_all_cells():
    cells = duckdb.sql("SELECT extracted.cell_type_label FROM rel").fetchall()
    return set(cells) # to make sure theyre not repeated

def get_cell_marker_pairs():
    return set(duckdb.sql("SELECT extracted.cell_type_label, extracted.gene FROM rel").fetchall())

def get_evidence():
    return duckdb.sql("SELECT * FROM rel").fetchall()

print(get_evidence())