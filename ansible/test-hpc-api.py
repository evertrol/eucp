from xml.etree import ElementTree as ET
import oca

ADDRESS = 'https://api.hpccloud.surfsara.nl/RPC2'
client = oca.Client(None, address=ADDRESS)
print(client.version())
