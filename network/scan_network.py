#!/usr/bin/python

import socket
from netifaces import interfaces, ifaddresses, AF_INET
import re
import sys

def get_my_ip():
  result = []  
  print 'retrieving ip addresses ...'  
  for ifaceName in interfaces():
    addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
    if not addresses:
      continue;
    address = addresses[0]
    if address == 'No IP addr':
      continue
    if ifaceName == 'lo':
      print 'Skip local: ', address 
      continue
    match = re.search(r'tap', ifaceName)
    if match:
      print 'Skip vpn: ', address 
      continue
    result.append(address)
  print 'found:',', '.join(result)
  return result

def check_ips(ip, maxip, ports):
  match = re.search(r'(\d+.\d+.+\d+).\d+', ip)
  if match: 
    ip_base = match.group(1)
    ip_base = ip_base+'.'
    ports_str = ', '.join(str(x) for x in ports)
    print 'checking network: ',ip_base+'1-'+str(maxip)+':'+ports_str
    for i in range(1,maxip):
      ip_to_check = ip_base+str(i)  
      check_ip_ports(ip_to_check, ports)

def check_ip_ports(ip, ports):
  for port in ports:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((ip,port))
    if result:
      continue
    print 'Ip:', ip, 'has open port', port

def num(s):
  try:
    return int(s)
  except ValueError:
    return 0

def main():
  args = sys.argv[1:]
  if not args:
    print "usage: [--max ip] port [port ...]";
    sys.exit(1)
  
  maxip = 0
  if args[0] == '--max':
    maxip = num(args[1])
    del args[0:2]

  if not maxip:
    maxip = 255
    
  if len(args) == 0:
    print "error: must specify one or more ports"
    sys.exit(1)

  ports = []
  for arg in args:
    port = num(arg)
    if port:
      ports.append(port)
  
  if len(ports) == 0:
    print "error: must specify one or more ports"
    sys.exit(1)

  ips = get_my_ip();
  for ip in ips:
    check_ips(ip, maxip, ports)  

if __name__ == "__main__":
  main()
