#!/usr/bin/env python3
# Adapted from Mark Mandel's implementation
# https://github.com/ansible/ansible/blob/devel/plugins/inventory/vagrant.py
# License: GNU General Public License, Version 3 <http://www.gnu.org/licenses/>

import argparse
import json
import paramiko
import subprocess
import sys
import io

def parse_args():
    parser = argparse.ArgumentParser(description="Vagrant inventory script")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true')
    group.add_argument('--host')

    return parser.parse_args()

def list_running_hosts():
    cmd = "vagrant status --machine-readable"
    status = subprocess.check_output(cmd.split(), text=True).rstrip()
    hosts = []

    for line in status.split('\n'):
        (_, host, key, value) = line.split(',',3)
        if key == 'state' and value == 'running':
            hosts.append(host)
    
    return hosts

def get_host_details(host):
    cmd = "vagrant ssh-config {}".format(host)
    
    # p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    # this_stdout = io.TextIOWrapper(p.stdout)
    # config = paramiko.SSHConfig()
    # config.parse(this_stdout)
    
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, text=True)
    config = paramiko.SSHConfig()
    config.parse(p.stdout)
    
    c = config.lookup(host)

    return {'ansible_ssh_host': c['hostname'],
            'ansible_ssh_port': c['port'],
            'ansible_ssh_user': c['user'],
            'ansible_ssh_private_key_file': c['identityfile'][0]}

def main():
    args = parse_args()
    if args.list:
        hosts = list_running_hosts()
        json.dump({'vagrant':hosts}, sys.stdout)
    else:
        details = get_host_details(args.host)
        json.dump(details, sys.stdout)

if __name__ == '__main__':
    main()
