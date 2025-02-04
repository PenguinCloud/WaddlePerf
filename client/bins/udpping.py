#!/usr/bin/env python3
# Original source inspiration https://github.com/wangyu-/UDPping/blob/master/udpping.py
# Cleaned up using CoPilot and migrated to Python 3.11

import sys
import time
import string
import random
import signal
import os
import getopt
import json
import socket
import logging
import base64

INTERVAL = 1000  # unit ms
LEN = 64
DSTHOST = "127.0.0.1"
PORT = 2000
PING_COUNT = 4  # Default count set to 4
OUTPUT_FILE = "udppingresults.json"  # Default output file
TTL = 64  # Default TTL value
LOG_LEVEL = logging.INFO  # Default logging level
TOKEN = None  # Default token value

count = 0
count_of_received = 0
rtt_sum = 0.0
rtt_min = float('inf')
rtt_max = 0.0

def signal_handler(signal, frame):
    if count != 0 and count_of_received != 0:
        logging.info('--- ping statistics ---')
    if count != 0:
        logging.info(f'{count} packets transmitted, {count_of_received} received, {(count - count_of_received) * 100.0 / count:.2f}% packet loss')
    if count_of_received != 0:
        logging.info(f'rtt min/avg/max = {rtt_min:.2f}/{rtt_sum / count_of_received:.2f}/{rtt_max:.2f} ms')
    write_statistics_to_json()
    os._exit(0)

def write_statistics_to_json():
    statistics = {
        'packets_transmitted': count,
        'packets_received': count_of_received,
        'packet_loss': (count - count_of_received) * 100.0 / count if count != 0 else 0,
        'rtt_min': rtt_min if count_of_received != 0 else None,
        'rtt_avg': rtt_sum / count_of_received if count_of_received != 0 else None,
        'rtt_max': rtt_max if count_of_received != 0 else None
    }
    with open(OUTPUT_FILE, 'w') as json_file:
        json.dump(statistics, json_file, indent=4)

def random_string(length):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def parse_options(options):
    global LEN, INTERVAL
    for option in options.split(';'):
        key, value = option.split('=')
        if key == 'LEN':
            LEN = int(value)
        elif key == 'INTERVAL':
            INTERVAL = int(value)

def main():
    global DSTHOST, PORT, PING_COUNT, OUTPUT_FILE, TTL, LOG_LEVEL, TOKEN, count, count_of_received, rtt_sum, rtt_min, rtt_max

    try:
        opts, args = getopt.getopt(sys.argv[1:], "a:c:o:p:f:t:l:k:h", ["address=", "count=", "options=", "port=", "file=", "ttl=", "loglevel=", "token=", "help"])
    except getopt.GetoptError as err:
        logging.error(str(err))
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-a", "--address"):
            DSTHOST = arg
        elif opt in ("-c", "--count"):
            PING_COUNT = int(arg)
        elif opt in ("-o", "--options"):
            parse_options(arg)
        elif opt in ("-p", "--port"):
            PORT = int(arg)
        elif opt in ("-f", "--file"):
            OUTPUT_FILE = arg
        elif opt in ("-t", "--ttl"):
            TTL = int(arg)
        elif opt in ("-l", "--loglevel"):
            LOG_LEVEL = getattr(logging, arg.upper(), logging.INFO)
        elif opt in ("-k", "--token"):
            TOKEN = arg
        elif opt in ("-h", "--help"):
            print("Usage: udpping.py -a <address or hostname> -c <count> -p <port> -f <output_file> -l <loglevel> -k <token>")
            sys.exit()
    if not DSTHOST or not PORT:
        print("Usage: udpping.py -a <address or hostname> -c <count> -p <port> -f <output_file> -l <loglevel> -k <token>")
        sys.exit(2)

    if LEN < 5:
        logging.error("LEN must be >=5")
        exit()
    if INTERVAL < 50:
        logging.error("INTERVAL must be >=50")
        exit()

    logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')

    signal.signal(signal.SIGINT, signal_handler)

    logging.info(f"UDPping {DSTHOST} via port {PORT} with {LEN} bytes of payload")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(INTERVAL / 1000.0)
    sock.setsockopt(socket.SOL_IP, socket.IP_TTL, TTL)

    while PING_COUNT is None or count < PING_COUNT:
        payload = random_string(LEN).encode()
        if TOKEN:
            encoded_token = base64.b64encode(TOKEN.encode()).decode()
            payload = f"{encoded_token}:{payload.decode()}".encode()
        time_of_send = time.perf_counter()
        sock.sendto(payload, (DSTHOST, PORT))
        deadline = time_of_send + INTERVAL / 1000.0
        received = 0
        rtt = 0.0

        try:
            while True:
                timeout = deadline - time.perf_counter()
                if timeout < 0:
                    break
                sock.settimeout(timeout)
                response, addr = sock.recvfrom(1024)
                if addr[0] == DSTHOST and addr[1] == PORT:
                    recv_time = time.perf_counter()
                    rtt = (recv_time - time_of_send) * 1000
                    logging.info(f"Reply from {DSTHOST} seq={count} time={rtt:.2f} ms")
                    received = 1
                    break
        except socket.timeout:
            pass

        count += 1
        if received == 1:
            count_of_received += 1
            rtt_sum += rtt
            rtt_max = max(rtt_max, rtt)
            rtt_min = min(rtt_min, rtt)
        else:
            logging.warning("Request timed out")

        time_remaining = deadline - time.perf_counter()
        if time_remaining > 0:
            time.sleep(time_remaining)

    signal_handler(None, None)

if __name__ == "__main__":
    main()
