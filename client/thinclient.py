#!/usr/bin/python3

import subprocess
import logging
import os
import sys
import getopt
import json_log_formatter

def configure_logging(log_to_console, log_file_path, log_as_json):
    handlers = []
    if log_to_console:
        handlers.append(logging.StreamHandler())
    else:
        handlers.append(logging.FileHandler(log_file_path))

    if log_as_json:
        formatter = json_log_formatter.JSONFormatter()
    else:
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')

    for handler in handlers:
        handler.setFormatter(formatter)

    logging.basicConfig(
        level=logging.INFO,
        handlers=handlers
    )

class ThinClient:
    def __init__(self):
        self.script_path = "vars/thinclientvariables.sh"
        self.playbook = "entrypoint.yml"
        self.webui_command = ["python3", "/workspaces/WaddlePerf/bins/webui.py", "8080"]

    def run_shell_script(self):
        if not os.path.isfile(self.script_path):
            logging.error(f"Script file {self.script_path} does not exist.")
            return

        command = ["bash", self.script_path]
        
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            logging.debug("Variables script executed successfully.")
        except subprocess.CalledProcessError as e:
            logging.error("Variables shell script failed.")
            logging.error(e.stderr)

    def validate_pping(self):
        command = ["pping", "--version"]
        
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            logging.debug("Install validated.")
        except subprocess.CalledProcessError:
            logging.error("Invalid installation of thin client. Exiting.")
            exit(1)

    def run_ansible_playbook(self):
        if not os.path.isfile(self.playbook):
            logging.error(f"Playbook file {self.playbook} does not exist.")
            return

        command = ["ansible-playbook", self.playbook, "-c", "local", "--tags", "thinclient"]
        
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            logging.debug("Playbook executed successfully.")
            logging.info(result.stdout)
        except subprocess.CalledProcessError as e:
            logging.error("Error executing playbook.")
            logging.error(e.stderr)

    def start_webui(self):
        try:
            subprocess.Popen(self.webui_command)
            logging.info("Web Client started in the background on port 8080.")
        except Exception as e:
            logging.error("Error starting Web Client.")
            logging.error(str(e))

def main(argv):
    log_to_console = False
    log_file_path = "logs/thinclient.log"
    log_as_json = False

    try:
        opts, args = getopt.getopt(argv, "hcj", ["help", "console", "logfile=", "json"])
    except getopt.GetoptError:
        print('Usage: thinclient.py [-c | --console] [--logfile=<path>] [-j | --json]')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('Usage: ./thinclient.py [-c | --console] [--logfile=<path>] [-j | --json]')
            sys.exit()
        elif opt in ("-c", "--console"):
            log_to_console = True
        elif opt == "--logfile":
            if not os.path.isdir(os.path.dirname(arg)):
                print(f"Log file directory {os.path.dirname(arg)} does not exist.")
                sys.exit(2)
            log_file_path = arg
        elif opt in ("-j", "--json"):
            log_as_json = True

    configure_logging(log_to_console, log_file_path, log_as_json)

    client = ThinClient()
    client.run_shell_script() # Run the shell script first
    client.validate_pping()   # Makes sure install script succeeded
    client.start_webui()      # Start the web UI in the background
    client.run_ansible_playbook()

if __name__ == "__main__":
    main(sys.argv[1:])