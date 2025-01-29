#!/usr/bin/python3

import subprocess

def validate_pping():
    command = ["pping", "--version"]
    
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        print("Install validated.")
    except subprocess.CalledProcessError:
        print("Invalid installation of thin client. Exiting.")
        exit(1)


def run_ansible_playbook():
    playbook = "entrypoint.yml"
    command = ["ansible-playbook", playbook, "-c", "local", "--tags", "thinclient"]
    
    try:
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("Playbook executed successfully.")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error executing playbook.")
        print(e.stderr)

def start_webui():
    command = ["python3", "/workspaces/WaddlePerf/bins/webui.py", "8080"]
    
    try:
        subprocess.Popen(command)
        print("Web UI started in the background on port 8080.")
    except Exception as e:
        print("Error starting Web UI.")
        print(str(e))

if __name__ == "__main__":
    validate_pping() # Makes sure install script succeded
    start_webui()    # Start the web UI in the background
    run_ansible_playbook()