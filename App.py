from flask import Flask, jsonify, render_template
from Database import get_recent

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/current')
def collect_metrics():
    data = get_recent()
    if len(data) == 0:
        return jsonify({"Error": "No content"}), 204
    else:
        return jsonify(data[0])

@app.route('/api/history')
def get_history():
    recent_data = get_recent()
    return jsonify(recent_data)

app.run(debug=True)