import pygeoip
from stem import CircStatus
from stem.control import Controller

gi = pygeoip.GeoIP('/home/jeff/cmu/14741/GeoIP.dat')
with Controller.from_port(port = 9051) as controller:
  controller.authenticate()

  for circ in sorted(controller.get_circuits()):
    if circ.status != CircStatus.BUILT:
      continue

    for i, entry in enumerate(circ.path):
      fingerprint, nickname = entry

      desc = controller.get_network_status(fingerprint, None)
      address = desc.address if desc else 'unknown'
      bandwidth = desc.bandwidth if desc else 'unknown'

      print "<%s, %s, %s kb/s>" % (address, gi.country_name_by_addr(address), bandwidth),
      if i != (len(circ.path) - 1): 
         print '-',
    print ''
