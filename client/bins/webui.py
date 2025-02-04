#! /usr/bin/env python3
# TODO: Get this working again for 4.1.0

# controllers.py
import json
import subprocess
from py4web import action, request, response, abort, redirect, URL
from py4web.core import Fixture
#from py4web.utils import websocket
from yatl.helpers import XML
from io import BytesIO
from ppingParser import ppingPerf as pping

class WebUI:
    def __init__(self):
        self.results = []
        self.ws = websocket('ws')

    @action('index')
    @action.uses('index.html')
    def index(self):
        return dict()

    @action('startiperf')
    def startiperf(self):
        result = subprocess.run(['iperf3-client'], capture_output=True, text=True)
        self.results.append(result.stdout)
        ws.send('update', result.stdout)
        return 'iPerf started'

    @action('startmttr')
    def startmttr(self):
        hostname = request.query.get('hostname')
        port = request.query.get('port')
        result = subprocess.run(['mttr', '-h', hostname, '-p', port], capture_output=True, text=True)
        self.results.append(result.stdout)
        websocket.send('update', result.stdout)
        return 'MTTR started'

    @action('startssh')
    def startssh(self):
        result = 'SSH not supported by webui yet'
        self.results.append(result)
        websocket.send('update', result)
        return 'SSH started'

    @action('starthttp')
    def starthttp(self):
        hostname = request.query.get('hostname')
        port = request.query.get('port')
        websocket.send('update', f"Starting HTTP request to {hostname}")
        pping_instance = pping(dstHost=hostname, dstPort=port)
        result = pping_instance.run()
        self.results.append(result)
        self.results.append(f"latencyMean: {result.latencyMean}\nlatencyMin: {result.latencyMin}\nlatencyMax: {result.latencyMax}")
        websocket.send('update', result)
        return 'HTTP started'

    @action('downloadresults')
    def downloadresults(self):
        json_data = json.dumps(self.results)
        response.headers['Content-Type'] = 'application/json'
        response.headers['Content-Disposition'] = 'attachment; filename=results.json'
        return json_data

    @websocket('ws')
    def ws(self, data):
        # This method will handle incoming websocket messages
        print(f"Received websocket message: {data}")
        websocket.send('update', f"Echo: {data}")

web_ui = WebUI()
