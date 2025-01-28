#!/usr/bin/env python3

import os
import sys
import getopt
import subprocess

def install_socat():
    subprocess.run(['apt', 'update'], check=True)
    subprocess.run(['apt', 'install', 'socat', '-y'], check=True)

def main(argv):
    try:
        opts, args = getopt.getopt(argv, "hp:a:", ["port=", "address="])
    except getopt.GetoptError:
        print('Usage: udpping-server.py -p <port> -a <address>')
        sys.exit(2)

    port = 2000
    address = '0.0.0.0'
    for opt, arg in opts:
        if opt == '-h':
            print('Usage: udpping-server.py -p <port> -a <address>')
            print('Example: udpping-server.py -p 2000 -a 0.0.0.0')
            print("Default port is 2000 and default address is  0.0.0.0")
            sys.exit()
        elif opt in ("-p", "--port"):
            port = arg
        elif opt in ("-a", "--address"):
            address = arg

    if subprocess.run(['socat', '-h'], capture_output=False).returncode == 0:
        print('socat installed')
    else:
        install_socat()
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((address, int(port)))

    print(f"Listening on UDP port {port} at address {address}")

    while True:
        data, addr = sock.recvfrom(1024)
        print(f"Received message: {data} from {addr}")
        sock.sendto(data, addr)

if __name__ == "__main__":
    main(sys.argv[1:])
