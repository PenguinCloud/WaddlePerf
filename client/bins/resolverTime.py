#! /usr/bin/env python3
import sys
import getopt
import socket
import time
import json
import statistics
import logging
import os
import dns
import dns.resolver

class DNSResolver:
    def __init__(self, domain, count, record_type='A', dns_server=None, output_file=None):
        self.domain = domain
        self.count = count
        self.record_type = record_type
        self.dns_server = dns_server
        self.output_file = output_file

    def resolve_dns(self):
        times = []
        resolve = None
        for _ in range(self.count):
            start_time = time.perf_counter()
            try:
                if self.dns_server:
                    resolve = dns.resolver.Resolver()
                    resolve.nameservers = [self.dns_server]
                    try:
                        resolve.resolve(self.domain, self.record_type)
                    except dns.resolver.NXDOMAIN:
                        print(f"Error: Domain '{self.domain}' not found.")
                        return []
                    except dns.resolver.Timeout:
                        print(f"Error: Timeout while querying '{self.dns_server}'.")
                        return []
                    except Exception as e:
                        print(f"An unexpected error occurred: {e}")
                        return []
                else:
                    socket.gethostbyname(self.domain)
                end_time = time.perf_counter()
                difference = end_time  - start_time
                times.append("%s" % difference)
            except Exception as e:
                print(f"An error occurred: {e} for domain {self.domain} recordType {self.record_type} on line {e.__traceback__.tb_lineno}")
                times.append(None)
        return times

    def run(self):
        if not self.domain:
            logging.error('Domain name is required')
            sys.exit(2)

        times = self.resolve_dns()
        # Remove all nones from the list
        times = [time for time in times if time is not None]
        result = {
            "domain": self.domain,
            "count": self.count,
            "record_type": self.record_type,
            "times": times,
            "min_time": min(times),
            "mean_time": statistics.mean([float(time) for time in times]),
            "max_time": max(times)
        }

        result_json = json.dumps(result, indent=4)
        logging.info(result_json)

        if self.output_file:
            with open(self.output_file, 'w') as f:
                f.write(result_json)
                

def main(argv):
    domain = ''
    count = 1
    record_type = 'A'
    dns_server = None
    output_file = None
    try:
        opts = getopt.getopt(argv, "hd:c:t:s:o:", ["domain=", "count=", "type=", "server=", "output="])[0]
    except getopt.GetoptError:
        logging.error('resolverTime.py -d <domain> -c <count> -t <record_type> -s <dns_server> -o <output_file>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            logging.info('resolverTime.py -d <domain> -c <count> -t <record_type> -s <dns_server> -o <output_file>')
            sys.exit()
        elif opt in ("-d", "--domain"):
            domain = arg
        elif opt in ("-c", "--count"):
            count = int(arg)
        elif opt in ("-t", "--type"):
            record_type = arg
        elif opt in ("-s", "--server"):
            dns_server = arg
        elif opt in ("-o", "--output"):
            output_file = arg

    resolver = DNSResolver(domain, count, record_type, dns_server, output_file)
    resolver.run()

if __name__ == "__main__":
    log_file = '/var/log/resolverTime.log' if os.name != 'nt' else 'resolverTime.log'
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ])
    main(sys.argv[1:])
