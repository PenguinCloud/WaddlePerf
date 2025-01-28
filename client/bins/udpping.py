#!/usr/bin/env python3
# Original source inspiration https://github.com/wangyu-/UDPping/blob/master/udpping.py
# Cleaned up using CoPilot and migrated to Python 3.11

import socket
import sys
import time
import string
import random
import signal
import os
import getopt
import json

INTERVAL = 1000  # unit ms
LEN = 64
IP = "127.0.0.1"
PORT = 2000
PING_COUNT = 4  # Default count set to 4
OUTPUT_FILE = "udppingresults.json"  # Default output file

count = 0
count_of_received = 0
rtt_sum = 0.0
rtt_min = float('inf')
rtt_max = 0.0

def signal_handler(signal, frame):
    if count != 0 and count_of_received != 0:
        print('')
        print('--- ping statistics ---')
    if count != 0:
        print(f'{count} packets transmitted, {count_of_received} received, {(count - count_of_received) * 100.0 / count:.2f}% packet loss')
    if count_of_received != 0:
        print(f'rtt min/avg/max = {rtt_min:.2f}/{rtt_sum / count_of_received:.2f}/{rtt_max:.2f} ms')
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
    global IP, PORT, PING_COUNT, OUTPUT_FILE, count, count_of_received, rtt_sum, rtt_min, rtt_max

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:c:o:p:f:", ["hostname=", "count=", "options=", "port=", "file="])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--hostname"):
            IP = arg
        elif opt in ("-c", "--count"):
            PING_COUNT = int(arg)
        elif opt in ("-o", "--options"):
            parse_options(arg)
        elif opt in ("-p", "--port"):
            PORT = int(arg)
        elif opt in ("-f", "--file"):
            OUTPUT_FILE = arg

    if not IP or not PORT:
        print("Usage: udpping.py -h <hostname> -c <count> -p <port> -f <output_file>")
        sys.exit(2)

    if LEN < 5:
        print("LEN must be >=5")
        exit()
    if INTERVAL < 50:
        print("INTERVAL must be >=50")
        exit()

    signal.signal(signal.SIGINT, signal_handler)

    is_ipv6 = ':' in IP
    sock = socket.socket(socket.AF_INET6 if is_ipv6 else socket.AF_INET, socket.SOCK_DGRAM)

    print(f"UDPping {IP} via port {PORT} with {LEN} bytes of payload")
    sys.stdout.flush()

    while PING_COUNT is None or count < PING_COUNT:
        payload = random_string(LEN)
        sock.sendto(payload.encode(), (IP, PORT))
        time_of_send = time.perf_counter()
        deadline = time_of_send + INTERVAL / 1000.0
        received = 0
        rtt = 0.0

        while True:
            timeout = deadline - time.perf_counter()
            if timeout < 0:
                break
            sock.settimeout(timeout)
            try:
                recv_data, addr = sock.recvfrom(65536)
                if recv_data == payload.encode() and addr[0] == IP and addr[1] == PORT:
                    rtt = (time.perf_counter() - time_of_send) * 1000
                    print(f"Reply from {IP} seq={count} time={rtt:.2f} ms")
                    sys.stdout.flush()
                    received = 1
                    break
            except socket.timeout:
                break
            except:
                pass
        count += 1
        if received == 1:
            count_of_received += 1
            rtt_sum += rtt
            rtt_max = max(rtt_max, rtt)
            rtt_min = min(rtt_min, rtt)
        else:
            print("Request timed out")
            sys.stdout.flush()

        time_remaining = deadline - time.perf_counter()
        if time_remaining > 0:
            time.sleep(time_remaining)

    signal_handler(None, None)

if __name__ == "__main__":
    main()
