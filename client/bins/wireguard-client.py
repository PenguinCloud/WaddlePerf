#!/usr/bin/env python3
# We eventually want to test tunneling for wireguard connections as well
import os
import subprocess
import platform
import getpass
import getopt
import sys

def get_user_input():
    username = None
    password = None
    cert_path = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:p:c:", ["username=", "password=", "cert_path="])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-u", "--username"):
            username = arg
        elif opt in ("-p", "--password"):
            password = arg
        elif opt in ("-c", "--cert_path"):
            cert_path = arg

    if not username or  not cert_path:
        print("Missing command line arguments, falling back to interactive input.")
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        cert_path = input("Enter path to the certificate: ")
    elif not password:
        password = getpass.getpass("Enter password: ")
    return username, password, cert_path

def establish_wireguard_connection(username, password, cert_path):
    system = platform.system().lower()
    wg_command = ""

    if system == "windows":
        wg_command = f'wireguard /installtunnelservice "{cert_path}"'
    elif system == "linux" or system == "darwin":  # darwin is for macOS
        wg_command = f'sudo wg-quick up "{cert_path}"'
    else:
        print(f"Unsupported OS: {system}")
        return

    try:
        env = os.environ.copy()
        env["WG_USER"] = username
        env["WG_PASS"] = password
        subprocess.run(wg_command, shell=True, check=True, env=env)
        print("WireGuard connection established successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to establish WireGuard connection: {e}")

if __name__ == "__main__":
    username, password, cert_path = get_user_input()
    establish_wireguard_connection(username, password, cert_path)