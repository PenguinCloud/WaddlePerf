# WaddlePerf

This is a project to allow for complete testing of user experience from one system to another.

This can be an endpoint testing it's internet connectivity, testing latency between regions, or even within cluster.

## AUTOPERF
All tests are given a tier number of 1-3

Our auto-perf mode runs any enabled tier 1 tests every X minutes defined by the deployer. 

It will then check to see if any upper bounds has been passed. If it has went over the upper bounds, tier 2 is ran.

If the tier 2 upper bounds are passed, it runs any defined tier 3 apps which are enabled.


Note, in autoperf mode, the tier has to be set and the tool must have been enabled.

## Results

Results are dropped to one or more of the following:
* Web Client Console
* S3 - if configured
* Syslog endpoints (coming in later versions)
* Central Management DB - if enterprise build and licensed

# Tests being ran
* Pping - https://github.com/wzv5/pping
* Httptrace - https://github.com/watson/http-traceroute
* HttpPing - https://github.com/folkertvanheusden/HTTPing
* Mtr - https://github.com/traviscross/mtr/
* SSHPing - https://github.com/spook/sshping
* MTU-Test - Our custom MTU tester which tests with DF to see what size of packet can be sent via ping
* UDP-PING - Our custom UDP ping client and server combination

# License
can be found in docs/LICENSE.md

# Contributing
can be found in docs/CONTRIBUTING.md

# Usage
can be found in docs/USAGE.md

All packages are scanned by socket.dev, snyk, and more to ensure security gold standard! 
However, if you find something we miss (we're only human), please open an issue or email us at: security@penguintech.io 

# Contributors
* PenguinzTech