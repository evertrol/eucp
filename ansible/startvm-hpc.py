import sys
from xml.etree import ElementTree as ET
import oca

ADDRESS = 'https://api.hpccloud.surfsara.nl/RPC2'
client = oca.Client(None, address=ADDRESS)

# [secret,] ID, name, hold/pending, extra-attrs, persistent
vmid = client.call('template.instantiate', 10377, 'server', False, 'memory=2048 cpu=2', False)
print(vmid)

