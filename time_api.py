# main.py
from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route('/time', methods=['GET'])
def get_time():
    current_time = datetime.utcnow().isoformat() + 'Z'
    return jsonify({'current_time': current_time})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)