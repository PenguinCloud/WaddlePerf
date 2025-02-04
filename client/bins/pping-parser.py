#!/usr/bin/env python3

from subprocess import Popen, PIPE, run
import sys
from getopt import getopt
from dataclasses import dataclass, asdict
from datetime import datetime
import logging
import subprocess
import json

@dataclass
class pping:
    datetime: str
    dstHost: str
    dstPort: int
    latencyMean: float
    latencyMin: float
    latencyMax: float
    dropped: int
    testtype: str

def setup_logging(log_file=None):
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if log_file:
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger

class ppingPerf:
    def __init__(self, logger):
        self.results: pping = pping(datetime=None, dstHost=None, dstPort=None, latencyMean=None, latencyMax=None, latencyMin=None,dropped=None, testtype=None)
        self.logger = logger
        self.results.dstPort = 80
        self.filePath = None

    def run(self):
        if len(sys.argv) < 2:
            self.logger.error("Usage: pping.py -t <testtype> -a <address> -p <port> -j <jsonfile>")
            sys.exit(1)
        try:
            opts, args = getopt(sys.argv[1:], "t:a:p:j:", ["testtype=", "address=", "port=", "jsonfile="])
        except:
            self.logger.error("Usage: pping.py -t <testtype> -a <address> -p <port> -j <jsonfile>")
            sys.exit(1)

        for opt, arg in opts:
            if opt in ("-t", "--testtype"):
                self.results.testtype = str(arg)
            elif opt in ("-a", "--address"):
                self.results.dstHost = str(arg)
            elif opt in ("-p", "--port"):
                self.results.dstPort = int(arg)
            elif opt in ("-j", "--jsonfile"):
                self.filePath = str(arg)

        if not self.results.testtype or not self.results.dstHost:
            self.logger.error("Usage: pping.py -t <testtype> -a <address> -p <port> -j <jsonfile>")
            sys.exit(1)
        now = datetime.now()
        self.results.datetime = now.strftime("%Y-%m-%d %H:%M:%S")
        self.results.dropped = 0
        self.results.latencyMean = 0.0
            
        if self.results.testtype in ['http', 'quic', 'tls', 'icmp']:
            self.logger.info("Running test: %s" % self.results.testtype)
            command = "pping %s %s"  % (self.results.testtype, self.results.dstHost)
            result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, _ = result.communicate()
            output = stdout
            results = self.parseHTTP(output)
        elif self.results.testtype == 'tcp':
            self.logger.info("Running TCP test: %s" % self.results.testtype)
            command = "pping %s %s %s" % (self.results.testtype, self.results.dstHost, self.results.dstPort)
            result = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, _ = result.communicate()
            output = stdout
            results = self.parseHTTP(output)
        else:
            self.logger.error("Invalid testtype: %s" % results.testtype)
            sys.exit(1)
            
        self.writeJSON()
        return results

    def writeJSON(self) -> None:
        if not self.filePath:
            self.filePath = "pping-%s-results.log" % self.results.testtype
        try:
            with open(self.filePath, 'w') as f:
                self.logger.debug(str(self.results))
                j = json.dumps(asdict(self.results), sort_keys=True, indent=4)
                f.write(j)
        except Exception as e:
            self.logger.error("Error writing to file: %s" % e)
            sys.exit(1)

    def parseHTTP(self, result: str) -> None: 
        import re
        latency = None
        dropped = None
        for line in result.splitlines():
            if "avg" in line:
                r = re.search(r'min \= (\d*) ms, max \= (\d*) ms, avg \= (\d*) ms', line)
                self.results.latencyMean = r.group(3)
                self.results.latencyMin = r.group(1)
                self.results.latencyMax = r.group(2)
            if "sent" in line:
                d = str(line.split(',')[2])
                d = d.strip()
                d = d.split('=')[1]
                self.results.dropped = int(d.split('(')[0])
        self.logger.info("LatencyMean: %s, LatencyMin: %s, LatencyMax: %s Dropped: %s" % (self.results.latencyMean, self.results.latencyMin, self.results.latencyMax, self.results.dropped))

    def parseLimited(self, result: str) -> None:
        import re
        for line in result.splitlines():
            if "avg" in line:
                self.logger.debug("Found AVG")
                r = re.search(r'min \= (\d*) ms, max \= (\d*) ms, avg \= (\d*) ms', line)
                self.results.latencyMean = r.group(3)
                self.results.latencyMin = r.group(1)
                self.results.latencyMax = r.group(2)
            if "sent" in line:
                self.logger.debug("Found Sent")
                d = str(line.split(',')[2])
                d = d.strip()
                d = d.split('=')[1]
                self.results.dropped = int(d.split('(')[0])
        self.logger.info("LatencyMean: %s, LatencyMin: %s, LatencyMax: %s Dropped: %s" % (self.results.latencyMean, self.results.latencyMin, self.results.latencyMax, self.results.dropped))
if __name__ == '__main__':
    log_file = None
    try:
        opts, args = getopt(sys.argv[1:], "l:", ["logfile="])
        for opt, arg in opts:
            if opt in ("-l", "--logfile"):
                log_file = arg
    except:
        pass

    logger = setup_logging(log_file)
    r = ppingPerf(logger)
    r.run()