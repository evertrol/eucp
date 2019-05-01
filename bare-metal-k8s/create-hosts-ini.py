#! /usr/bin/env python3

import sys
import argparse
from operator import itemgetter
from xml.etree import ElementTree as ET
import oca

ADDRESS = 'https://api.hpccloud.surfsara.nl/RPC2'
DEFAULT_TEMPLATE = 11483


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('basenames', nargs='*', default=['controller', 'worker'], help="Base names")
    args = parser.parse_args()
    return args


def poll(client, basenames):
    result = client.call('vmpool.info', -1, -1, -1, -1)
    root = ET.fromstring(result)

    nodes = []
    for node in root.findall('./VM/ID/..'):
        name = node.find('NAME').text
        for basename in basenames:
            if name.startswith(basename):
                break
        else:
            continue
        state = (int(node.find('STATE').text),
                 int(node.find('LCM_STATE').text))
        if state != (3, 3):
            return False

        nodes.append({'id': int(node.find('ID').text),
                      'name': name,
                      'ip': node.find('TEMPLATE/CONTEXT/ETH0_IP').text,
                      'state': (int(node.find('STATE').text),
                                int(node.find('LCM_STATE').text)),
        })

    nodes.sort(key=itemgetter('name'))
    return nodes


def write_host_ini(nodes):
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
    print(text)


def main(basenames):
    client = oca.Client(None, address=ADDRESS)

    # Python 3.8:
    # while not nodes := poll(client, basenames): pass
    while True:
        nodes = poll(client, basenames)
        if nodes:
            break

    write_host_ini(nodes)


if __name__ == '__main__':
    args = parse_args()
    main(args.basenames)
