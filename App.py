from flask import Flask, jsonify, render_template
from Database import get_recent
from Status import check_alerts

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

@app.route('/api/status')
def get_status():
    try:
        status = check_alerts()
        return jsonify(status) 
    except Exception as e:
        return jsonify({"error": str(e)}), 500 

app.run(debug=True)