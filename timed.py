import socket
import socks
import time
import urllib
from stem import Signal
from stem.control import Controller
import stem.process
from stem.util import term

def print_bootstrap_lines(line):
   if "Bootstrapped " in line:
      print term.format(line, term.Color.BLUE)

def getaddrinfo(*args):
   return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

def query(url):
   try:
      return urllib.urlopen(url).read()
   except:
      return "Unable to reach %s" % url

def test():
   host = 'www.duckduckgo.com'
   port = 80
   s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   s.connect((host, port))
   start = time.clock()
   s.send("""GET / HTTP/1.0\r
   Host: www.duckduckgo.com\r\n\r\n""")
   data = s.recv(1024)
   while data != '':
      data = s.recv(1024)
   end = time.clock()
   s.close()
   #print "clearnet time:"
   cleartime = end-start
   print cleartime,
   print ',', 

   SOCKS_PORT = 7000
   socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', SOCKS_PORT)
   socket.socket = socks.socksocket

   socket.getaddrinfo = getaddrinfo
   tor = stem.process.launch_tor_with_config(
      config = {
         'SocksPort': str(SOCKS_PORT)
      }
      #init_msg_handler = print_bootstrap_lines,
   )
   start = time.clock()
   data = query("http://3g2upl4pq6kufc4m.onion")
   end = time.clock()
   #print 'tor time:'
   tortime = end-start
   print tortime,
   print ',',
   tor.kill()
   #print 'delta:'
   print tortime-cleartime,
   print ',',
   #print 'magnitude'
   print tortime/cleartime,
   print ',',
   tor = stem.process.launch_tor_with_config(
      config = {
         'SocksPort': str(SOCKS_PORT)
      }
      #init_msg_handler = print_bootstrap_lines,
   )
   start = time.clock()
   data = query("http://duckduckgo.com")
   end = time.clock()
   #print "tor to clearnet address time:"
   print end-start
   tor.kill()


for x in range(1,2):
   print x,
   print ',',
   test()
