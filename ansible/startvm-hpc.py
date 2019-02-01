import sys
import argparse
from xml.etree import ElementTree as ET
import oca

ADDRESS = 'https://api.hpccloud.surfsara.nl/RPC2'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--memory', default=2048, type=int, help="Memory (MB)")
    parser.add_argument('-c', '--cpu', default=2, type=int, help="Number of CPU cores")
    args = parser.parse_args()
    return args


def main(memory=2048, cpu=2):
    options = f"memory={memory} cpu={cpu}"

    client = oca.Client(None, address=ADDRESS)
    # [secret,] ID, name, hold/pending, extra-attrs, persistent
    vmid = client.call('template.instantiate', 10377, 'server', False, options, False)
    print("Started VM with ID =", vmid)


if __name__ == '__main__':
    args = parse_args()
    main(memory=args.memory, cpu=args.cpu)
