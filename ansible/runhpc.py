import sys
from xml.etree import ElementTree as ET
import oca

ADDRESS = 'https://api.hpccloud.surfsara.nl/RPC2'
client = oca.Client(None, address=ADDRESS)

r = client.call('vmpool.info', -1, -1, -1, -1)
root = ET.fromstring(r)
ET.dump(root)

id = root.find('VM/ID').text
print('VM ID =', id)

r, s, t = client.call('vm.action', sys.argv[1], int(id))
print(r, s, t)
