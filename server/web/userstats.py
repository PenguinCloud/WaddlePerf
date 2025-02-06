#!/usr/bin/env python3
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/ip', methods=['GET'])
def ip():
    client_ip = request.remote_addr
    return jsonify({'ip': client_ip})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

