#!/usr/bin/env python3
import getopt
import sys
import json
from flask import Flask, render_template_string, jsonify, send_file
from io import BytesIO

class WebUI:
    def __init__(self, port=5000):
        self.app = Flask(__name__)
        self.port = port
        self.setup_routes()
        self.results = []

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template_string('''
                <html>
                <head>
                    <title>WaddlePerf Web Client</title>
                    <style>
                        body {
                            background-color: black;
                            color: green;
                            text-align: left;
                            margin-top: 50px;
                        }
                        button {
                            margin: 10px;
                            padding: 10px 20px;
                            font-size: 16px;
                            background-color: black;
                            border: 2px solid green;
                            color: green;
                            font-weight: bold;
                        }
                        #response-box {
                            margin-top: 20px;
                            padding: 10px;
                            border: 1px solid green;
                            height: 200px;
                            overflow-y: scroll;
                            white-space: pre-wrap;
                            text-align: left;
                        }
                    </style>
                    <script>
                        function fetchAndDisplay(endpoint) {
                            fetch(endpoint)
                                .then(response => response.text())
                                .then(data => {
                                    const responseBox = document.getElementById('response-box');
                                    responseBox.textContent += data + '\\n';
                                    responseBox.scrollTop = responseBox.scrollHeight;
                                });
                        }

                        function downloadResults() {
                            window.location.href = '/downloadresults';
                        }
                    </script>
                </head>
                <body>
                    <div id="control-box">
                    <h1>WaddlePerf Web Client</h1>
                    <button onclick="fetchAndDisplay('/startiperf')">Start iPerf</button>
                    <button onclick="fetchAndDisplay('/startmttr')">Start MTTR</button>
                    <button onclick="fetchAndDisplay('/startssh')">Start SSH</button>
                    <button onclick="fetchAndDisplay('/starthttp')">Start HTTP</button>
                    <button onclick="downloadResults()">Download Results</button>
                    </div>
                    <div id="response-header"><h2>Results:</h2><br /></div>
                    <div id="response-box" width="%100"></div>
                </body>
                </html>
            ''')

        @self.app.route('/startiperf')
        def startiperf():
            result = 'iPerf started'
            self.results.append(result)
            return result

        @self.app.route('/startmttr')
        def startmttr():
            result = 'MTTR started'
            self.results.append(result)
            return result

        @self.app.route('/startssh')
        def startssh():
            result = 'SSH started'
            self.results.append(result)
            return result

        @self.app.route('/starthttp')
        def starthttp():
            result = 'HTTP started'
            self.results.append(result)
            return result

        @self.app.route('/downloadresults')
        def downloadresults():
            json_data = json.dumps(self.results)
            return send_file(BytesIO(json_data.encode()), mimetype='application/json', as_attachment=True, attachment_filename='results.json')

    def run(self):
        self.app.run(debug=True, port=self.port)

def main(argv):
    port = 5000  # Default port
    try:
        opts, args = getopt.getopt(argv, "hp:", ["port="])
    except getopt.GetoptError:
        print('webui.py -p <port>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('webui.py -p <port>')
            sys.exit()
        elif opt in ("-p", "--port"):
            port = int(arg)
    web_ui = WebUI(port)
    web_ui.run()

if __name__ == '__main__':
    main(sys.argv[1:])