from flask import Flask, jsonify, render_template
from Monitor import collect
from Database import get_recent

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/current')
def collect_metrics():
    data = collect()
    if data is None:
        return jsonify({"Error": "Failed to collect metrics"}), 500
    return jsonify(data)

@app.route('/api/history')
def get_history():
    recent_data = get_recent()
    return jsonify(recent_data)

app.run(debug=True)