#!/usr/bin/python3

from pydal import DAL, Field, IS_IPADDRESS, IS_ALPHANUMERIC, IS_LENGTH, IS_IN_SET
from dataclasses import dataclass


@dataclass
class dbInfo: 
    dbName: str = 'waddleperf'
    dbUser: str = 'waddler'
    dbPass: str = ''
    dbHost: str = 'localhost'
    dbPort: str = '5432'
    dbType: str = 'mysql'
    

@dataclass
class perfInfo:
    testName: str
    testType: str
    testDstHost: str
    testSrcHost: str
    testHost: str
    avgLatency: float
    avgThroughput: float
    avgJitter: float
    avgPacketLoss: float

class dbConnect:
    def __init__(self, dbInfo):
        self.db = DAL(dbInfo.DbType+'://'+dbInfo.dbUser+':'+dbInfo.dbPass+'@'+dbInfo.dbHost+':'+dbInfo.dbPort+'/'+dbInfo.dbName)
        self.db.define_table('testResults', 
                             Field('testName', 'string', required=True, requires = IS_ALPHANUMERIC()),
                             Field('testType', 'string', required=True, requires = IS_IN_SET(['sshping', 'iperf', 'httptrace', 
                                                                                              'pping-dns', 'pping-quic', 'pping-tcp', 
                                                                                              'pping-tls', 'pping-http',
                                                                                              'traceroute','mtr', 'ping'])), 
                             Field('testHost', 'string', required=True, requires = IS_ALPHANUMERIC(), label='hostname which the test was for'), 
                             Field('testDstHost', 'string', requires = IS_IPADDRESS(), label='Acting Server host for testing'), 
                             Field('testSrcHost', 'string', requires = IS_IPADDRESS(), label='Client host for testing'), 
                             Field('avgLatency', 'float', requires=IS_LENGTH(3, 12)), 
                             Field('avgThroughput', 'float', requires=IS_LENGTH(3, 12)), 
                             Field('avgJitter', 'float', requires=IS_LENGTH(3, 12)), 
                             Field('avgPacketLoss', 'float', requires=IS_LENGTH(3, 12)))
    
    def insertPerfData(self, perfInfo):
        self.db.testResults.insert(testName=perfInfo.testName, 
                                   testType=perfInfo.testType, 
                                   testDstHost=perfInfo.testDstHost, 
                                   testSrcHost=perfInfo.testSrcHost, 
                                   avgLatency=perfInfo.avgLatency, 
                                   avgThroughput=perfInfo.avgThroughput, 
                                   avgJitter=perfInfo.avgJitter, 
                                   avgPacketLoss=perfInfo.avgPacketLoss)
    
    def queryTestName(self, testName):
        return self.db(self.db.testResults.testName == testName).select()
    
    def queryHostName(self, hostName):
        return self.db((self.db.testResults.testDstHost == hostName) | (self.db.testResults.testSrcHost == hostName)).select()
    
    def close(self):
        self.db.close()
        
class logParser():
    def __init__(self, logFile):
        self.result = perfInfo
        self.logFile = logFile
        
    def iperf(self):
        with open(self.logFile, 'r') as file:
            perfData= json.load(file)
            file.close
        # TODO: CHange test name to be something onboarded as like a description later
        self.result.testName = "iperf"
        self.result.testType = "iperf"
        # TODO: Change this to be more dynamic later from request
        self.result.testHost = "nohost.local"
        self.result.testDstHost = perfData['server_ip']
        self.result.testSrcHost = perfData['client_ip']
    
                    
        return self.result