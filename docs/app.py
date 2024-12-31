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
    df = conn.execute("SELECT * FROM evidence").fetch_df()
    return jsonify(df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)