import sqlite3
import json

conn = sqlite3.connect('evidence.db')
#conn.execute("CREATE TABLE evidence_table (organism text, cell_source text, cell_type text, cell_state text, gene text, gene_id text);")
with open('evidence.json', 'r') as json_file:
    data = json.load(json_file)
    for item in data:
        conn.execute("INSERT INTO evidence_table (organism, cell_source, cell_type, cell_state, gene, gene_id) VALUES (?,?,?,?,?,?)", (item['organism'], item['cell_source'], item['cell_type'], item['cell_state'], item['gene'], item['gene_id']))
conn.commit()
conn.close()