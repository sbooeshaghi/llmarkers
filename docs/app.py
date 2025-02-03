# using Python Flask backend to connect to DuckDB database

# in terminal: flask run

import duckdb
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

conn = duckdb.connect("evidence.db")

@app.route('/')
def index():
    return 'this is our website!' # for testing purposes; can delete later

@app.route('/evidence')
def get_evidence():
    df = conn.execute("SELECT a.doi,a.citation,s.organism,c.cell_source,c.cell_type_label,c.cell_state,g.gene,g.ensembl_id,s.source_type,s.source_rationale FROM Derived d LEFT JOIN Gene g ON d.gene_id = g.gene_id LEFT JOIN Article a ON d.article_id = a.article_id LEFT JOIN Cell c ON d.cell_id = c.cell_id LEFT JOIN Source s ON d.derived_id = s.derived_id;").fetch_df()
    return jsonify(df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)