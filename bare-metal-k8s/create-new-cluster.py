#! /usr/bin/env python3

import sys
import os
import argparse
from operator import itemgetter
from tempfile import NamedTemporaryFile
import shutil
from xml.etree import ElementTree as ET
import oca

ADDRESS = 'https://api.hpccloud.surfsara.nl/RPC2'
DEFAULT_TEMPLATE = 11483


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('nnodes', type=int, nargs='?', help="Number of nodes")
    parser.add_argument('-t', '--template', default=DEFAULT_TEMPLATE, help="Template ID")
    parser.add_argument('-m', '--memory', default=3072, type=int, help="Memory (MB)")
    parser.add_argument('-c', '--cpu', default=2, type=int, help="Number of CPU cores")
    parser.add_argument('-C', '--vcpu', default=2, type=int,
                        help="Number of virtual CPU cores")
    parser.add_argument('-H', '--hosts', default='hosts.ini',
                        help="Output Ansible hosts file name")
    args = parser.parse_args()
    return args


def poll(client, vmids):
    result = client.call('vmpool.info', -1, -1, -1, -1)
    root = ET.fromstring(result)

    nodes = []
    for node in root.findall('./VM/ID/..'):
        idx = int(node.find('ID').text)
        if idx not in vmids:
            continue
        state = (int(node.find('STATE').text),
                 int(node.find('LCM_STATE').text))
        if state != (3, 3):
            return False

        nodes.append({'id': int(node.find('ID').text),
                      'name': node.find('NAME').text,
                      'ip': node.find('TEMPLATE/CONTEXT/ETH0_IP').text,
                      'state': (int(node.find('STATE').text),
                                int(node.find('LCM_STATE').text)),
        })

    nodes.sort(key=itemgetter('name'))
    return nodes


def write_host_ini(nodes, filename='hosts.ini'):
    workers = []
    text = ["[all]"]
    for i, node in enumerate(nodes):
        text.append(f"node{i} ansible_host={node['ip']}")
        if node['name'] == 'controller':
            controller = f"node{i}"
        else:
            workers.append(f"node{i}")
    text.extend(["", "[controller]", controller])
    text.extend(["", "[workers]"] + workers)

    text = "\n".join(text)
    if filename:
        with open(filename, 'w') as fp:
            fp.write(text + "\n")
    else:
        print(text)


def update_ssh_config(nodes):
    path = os.path.expanduser("~/.ssh/config")
    try:
        with open(path) as fp, NamedTemporaryFile(mode="w", delete=False) as tmp:
            ip = None
            for line in fp:
                if 'knode' in line:
                    inode = int(line[10:])
                    ip = nodes[inode]['ip']
                elif ip and 'HostName' in line:
                    line = f"  HostName = {ip}\n"
                    ip = None
                tmp.write(line)
        shutil.move(tmp.name, path)
    except FileNotFoundError:
        pass


def update_known_hosts(nodes):
    path = os.path.expanduser("~/.ssh/known_hosts")
    ips = [node['ip'] for node in nodes]
    try:
        with open(path) as fp, NamedTemporaryFile(mode="w", delete=False) as tmp:
            for line in fp:
                ip = line.split()
                if ip in ips:
                    continue
                tmp.write(line)
        shutil.move(tmp.name, path)
    except FileNotFoundError:
        pass


def main(nnodes, templateid=DEFAULT_TEMPLATE, memory=2048, cpu=2, vcpu=2,
         output='hosts.ini'):
    client = oca.Client(None, address=ADDRESS)

    if not nnodes:
        result = client.call('templatepool.info', -3, -1, -1)
        root = ET.fromstring(result)
        defname = None
        for node in root.findall('./VMTEMPLATE'):
            idx = int(node.find('ID').text)
            name = node.find('NAME').text
            print(f"Template {name}: id = {idx}")
            if idx == DEFAULT_TEMPLATE:
                defname = name
        if defname:
            print(f"Default template = {defname} (id = {DEFAULT_TEMPLATE})")
        return

    options = f"memory={memory} cpu={cpu} vcpu={vcpu}"
    vmids = []
    for i in range(nnodes):
        name = 'controller' if i == 0 else f'worker{i}'
        # [secret,] ID, name, hold/pending, extra-attrs, persistent
        vmid = client.call('template.instantiate', templateid, name, False, options, False)
        vmids.append(vmid)

    # Python 3.8:
    # while not nodes := poll(client, vmids): pass
    while True:
        nodes = poll(client, vmids)
        if nodes:
            break

    write_host_ini(nodes, output)
    update_ssh_config(nodes)
    update_known_hosts(nodes)


if __name__ == '__main__':
    args = parse_args()
    main(args.nnodes, memory=args.memory, cpu=args.cpu, vcpu=args.vcpu,
         output=args.hosts)
