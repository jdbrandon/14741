import socket
import socks
import time
import urllib
from stem import Signal
from stem.control import Controller
import stem.process
from stem.util import term

host = 'www.google.com'
port = 80

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
start = time.clock()
s.send("""GET / HTTP/1.0\r
Host: www.google.com\r\n\r\n""")
data = s.recv(1024)
end = time.clock()
s.close()
#print data
print "clearnet time:"
print end-start

def print_bootstrap_lines(line):
   if "Bootstrapped " in line:
      print term.format(line, term.Color.BLUE)

SOCKS_PORT = 7000

socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', SOCKS_PORT)
socket.socket = socks.socksocket

def getaddrinfo(*args):
   return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

socket.getaddrinfo = getaddrinfo

def query(url):
   try:
      return urllib.urlopen(url).read()
   except:
      return "Unable to reach %s" % url

tor = stem.process.launch_tor_with_config(
   config = {
      'SocksPort': str(SOCKS_PORT)
   },
   init_msg_handler = print_bootstrap_lines,
)
start = time.clock()
data = query("https://www.google.com")
end = time.clock()
print end-start
tor.kill()
