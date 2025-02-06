#!/usr/bin/env python3
from flask import Flask, request, jsonify, send_file, render_template_string
import subprocess
import os
import json
from io import BytesIO
import psutil

app = Flask(__name__)
app.env = 'production'
class WebUI:
    def __init__(self):
        self.results = []

webui = WebUI()

@app.route('/')
def index():
    return render_template_string('''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8">
            <title>WebUI</title>
            <style>
                body {
                    background-color: black;
                    color: green;
                }
                select, button, input {
                    color: green;
                    border: 1px solid green;
                    background-color: black;
                }
            </style>
        </head>
        <body>
            <h1>Initiate a Test </h1>
            <form id="scriptForm">
                <label for="script">Choose a script:</label>
                <select id="script" name="script">
                    <option value="ppingParser.py">ppingParser.py</option>
                    <option value="udpping.py">udpping.py</option>
                    <option value="iperf3">iperf3</option>
                </select>
                <br><br>
                <label for="arguments">Arguments:</label>
                <input type="text" id="arguments" name="arguments" placeholder="Enter arguments">
                <br><br>
                <button type="button" onclick="startScript()">Start Script</button>
            </form>
            <div id="results"></div>
            <script>
                function startScript() {
                    const script = document.getElementById('script').value;
                    const args = document.getElementById('arguments').value;
                    fetch('/startscript', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ script_name: script, arguments: args })
                    })
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('results').innerText = data.output || data.error;
                    });
                }
            </script>
        </body>
        </html>
    ''')

@app.route('/startscript', methods=['POST'])
def startscript():
    script_name = request.json.get('script_name')
    argument = request.json.get('arguments')
    script_path = os.path.join('bins', script_name)
    if not os.path.isfile(script_path) and script_name != 'iperf3':
        return jsonify({'error': 'Script not found'}), 404

    if script_name == 'iperf3':
        result = subprocess.run(['iperf3', argument], capture_output=True, text=True)
    else:
        result = subprocess.run(['python3', script_path, argument], capture_output=True, text=True)
    
    webui.results.append(result.stdout)
    return jsonify({'output': result.stdout})

@app.route('/downloadresults')
def downloadresults():
    json_data = json.dumps(webui.results)
    response = BytesIO()
    response.write(json_data.encode('utf-8'))
    response.seek(0)
    return send_file(response, as_attachment=True, download_name='results.json', mimetype='application/json')

@app.route('/clientstats')
def clientstats():
    # result = subprocess.run(['python3', 'bins/clientstats.py'], capture_output=True, text=True)
    cpuResult = psutil.cpu_percent(interval=1)
    diskResult = psutil.disk_usage
    memoryResult = psutil.virtual_memory().percent
    return jsonify({'cpu': cpuResult, 'disk': diskResult, 'memory': memoryResult})
if __name__ == '__main__':
    app.run(debug=True, port=5050, host="0.0.0.0")
