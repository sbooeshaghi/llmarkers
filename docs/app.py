# using Python Flask backend to connect to DuckDB database

# in terminal: flask run

import duckdb
from flask import Flask, jsonify

app = Flask(__name__)

conn = duckdb.connect("evidence.db")

@app.route('/')
def index():
    return 'this is our website!' # for testing purposes; can delete later

@app.route('/evidence')
def get_evidence():
    result = conn.execute("SELECT * FROM evidence").fetchall()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)