#! /bin/bash

# Run ansibble playbook
ansible-playbook client.yml -c local -i localhost, -e "ansible_python_interpreter=/usr/bin/python3"