#!/usr/bin/python3
# Quick script written for now... will wrap back and clean up eventually
import json
import sys
class httptrace:
    def ___init__(filename):
        self.filename = filename
        self.hops = []
        self.totalLatency = ""
        self.totalHop = ""
    def getTime(self):
        from datetime import datetime
        return datetime.utcnow().timestamp()
  
    def removeBraces(self, blob):
        from regex import match
        return match(r"^\(([A-Za-z 0-9]*)\)$", blob)
    def readfile(self):
        try:
            with open(self.filename, 'r') as tracefile:
                contents = tracefile.readlines()
            for line in contents:
                linelist = line.split()
                latency = ""
                for element in linelist:
                    if "ms" in element:
                        latency = self.removeBraces(element)
                if len(latency) > 0:
                    self.hops.append({ "host": linelist[3], "code":linelist[0], "version":linelist[1], "latency":latency })
                if "finished" in line:
                    self.totalLatency = linelist[3]
                    self.totalHop = linelist[6]
        except Exception as err:
            print(err)
    def writeJson(self):
        toFile = { "total": self.totalLatency, "count": self.totalHop,  "hops": self.hops}
        try:
            jsonFilename = "httptrace-%s.json" % self.getTime()
            with open(jsonFilename, 'w') as jsonFile:
                json.dump(toFile, indent=4)
        except Exception as err:
            print(err)
if __name__ == '__main__':
    if len(sys.argv) > 0:
        jsonObj = httptrace.__init__(sys.argv[1])
    else:
        jsonObj = httptrace.__init__("httptrace.log")
