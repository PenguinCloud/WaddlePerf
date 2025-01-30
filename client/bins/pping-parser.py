#!/usr/bin/python3

from subprocess import Popen, PIPE, run
import sys
from getopt import getopt
from dataclasses import dataclass
from datetime import datetime
import logging

@dataclass
class pping:
    datetime: str
    dstHost: str
    dstPort: int
    latency: float
    dropped: int
    testtype: str

def setup_logging(log_file=None):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if log_file:
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger

# This function will run the pping command and write the results to a file
def ppingResults(logger):
    if len(sys.argv) < 2:
        logger.error("Usage: pping.py -t <testtype> -a <address> -p <port> -l <logfile>")
        sys.exit(1)
    try:
        opts, args = getopt(sys.argv[1:], "t:a:p:l:", ["testtype=", "address=", "port=", "logfile="])
    except:
        logger.error("Usage: pping.py -t <testtype> -a <address> -p <port> -l <logfile>")
        sys.exit(1)
    testType = None
    host = None
    port = None

    for opt, arg in opts:
        if opt in ("-t", "--testtype"):
            testtype = arg
        elif opt in ("-a", "--address"):
            host = arg
        elif opt in ("-p", "--port"):
            port = arg

    if not testtype or not host:
        logger.error("Usage: pping.py -t <testtype> -a <address> -p <port> -l <logfile>")
        sys.exit(1)

    results = pping(datetime=datetime.now, dstHost=host, dstPort=port, latency=0.0, testtype=testtype, dropped=0)

    if testtype in ['http', 'quic', 'tls', 'icmp']:
        results.dstPort = int(host.split(':')[1]) if ':' in host else 0
        results.dstPort = 53
        result = run(['pping', testtype, results.dstHost], stdout=PIPE)
    elif testtype == 'tcp':
        if not port:
            logger.error("Usage: pping.py -m tcp -h <host> -p <port>")
            sys.exit(1)
        results.dstPort = int(port)
        results.dropped = (line.split(',')[4]).split('=')[1]
        result = run(['pping',results.testtype, results.dstHost, results.dstPort], stdout=PIPE)
    else:
        logger.error("Invalid testtype: %s" % results.testtype)
        sys.exit(1)
        
    # define the filename
    filename = "pping-%s-results.log" % results.testtype
    try:
        with open(filename, 'w') as f:
            f.write(results.stdout.decode('utf-8'))
            f.close()
    except Exception as e:
        logger.error("Error writing to file: %s" % e)
        sys.exit(1)
    for line in result.stdout.decode('utf-8'):
        for line in result.stdout.decode('utf-8').splitlines():
            if "avg" in line:
                results.latency = float((line.split(',')[6]).split('=')[1])
                results.dropped = int((line.split(',')[4]).split('=')[1])
                latency = (line.split(',')[6]).split('=')[1]
                f.writeline(latency)
    return results

def ppingResultsDict(logger):
    results = ppingResults(logger)
    return results.__dict__
                
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
    ppingResults(logger)