#!/usr/bin/python3

from subprocess import Popen, PIPE, run
import sys
from dataclasses import dataclass


@dataclass
class pping:
    datetime: str
    dstHost: str
    dstPort: int
    latency: float
    method: str
    droppped: int

# This function will run the pping command and write the results to a file
def ppingResults():
    if len(sys.argv) < 2:
        print("Usage: pping.py <method> <host> <:port>")
        sys.exit(1)
    results = pping
    results.method = sys.argv[1]
    results.dstHost = sys.argv[2].split(':')[0]
    
    # Split it out by method to determine how to handle, note ICMP doesnt have a port so it doesnt matter what we throw in there
    if results.method == 'http' or result.method == 'quic' or results.method == 'tls' or results.method == 'icmp':
        results.dstPort = sys.argv[2].split(':')[1]
        result = run(['pping',results.method, results.dstHost], stdout=PIPE)
    elif results.method == 'dns':
        results.dstPort = 53
        result = run(['pping',results.method, results.dstHost], stdout=PIPE)
    elif results.method == 'tcp':
        results.dstPort = sys.argv[3]
        result = run(['pping',results.method, results.dstHost, results.dstPort], stdout=PIPE)
    else:
        print("Invalid method: %s" % results.method)
        sys.exit(1)
        
    # define the filename
    filename = "pping-%s-results.log" % results.method
    try:
        with open(filename, 'w') as f:
            f.write(results.stdout.decode('utf-8'))
            f.close()
    except Exception as e:
        print("Error writing to file: %s" % e)
        sys.exit(1)
    for line in result.stdout.decode('utf-8'):
        if "avg" in line:
            results.latency = (line.split(',')[6]).split('=')[1]
            results.droppped = (line.split(',')[4]).split('=')[1]
            latency = (line.split(',')[6]).split('=')[1]
            f.writeline(latency)
    return results

def ppingResultsDict():
    results = ppingResults()
    return results.__dict__
                
if __name__ == '__main__':
    ppingResults()