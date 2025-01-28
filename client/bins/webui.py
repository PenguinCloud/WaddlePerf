#!/usr/bin/env python3
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
        <html>
        <head>
            <title>Web UI</title>
            <style>
                body {
                    background-color: black;
                    color: white;
                    text-align: center;
                    margin-top: 50px;
                }
                button {
                    margin: 10px;
                    padding: 10px 20px;
                    font-size: 16px;
                }
            </style>
        </head>
        <body>
            <h1>Web UI</h1>
            <button onclick="fetch('/startiperf')">Start iPerf</button>
            <button onclick="fetch('/startmttr')">Start MTTR</button>
            <button onclick="fetch('/startssh')">Start SSH</button>
            <button onclick="fetch('/starthttp')">Start HTTP</button>
        </body>
        </html>
    ''')

@app.route('/startiperf')
def startiperf():
    # Implement your startiperf function here
    return 'iPerf started'

@app.route('/startmttr')
def startmttr():
    # Implement your startmttr function here
    return 'MTTR started'

@app.route('/startssh')
def startssh():
    # Implement your startssh function here
    return 'SSH started'

@app.route('/starthttp')
def starthttp():
    # Implement your starthttp function here
    return 'HTTP started'

if __name__ == '__main__':
    app.run(debug=True)