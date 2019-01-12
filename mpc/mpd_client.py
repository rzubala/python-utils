#!/usr/bin/env python

import sys
from mpd import MPDClient

def connect(ip, port):
  client = MPDClient()
  client.timeout = 60     # network timeout in seconds (floats allowed), default: None
  client.idletimeout = None
  client.connect(ip, port)
  return client

def stop(ip, port):
  client = connect(ip, port)
  client.clear()
  return client

def play(ip, port, url):
  client = stop(ip, port)  
  client.add(url)
  client.play()

def print_status(ip, port):
  client = connect(ip, port)
  print client.status()  

def num(s):
  try:
    return int(s)
  except ValueError:
    return 0

def main():
  args = sys.argv[1:]
  if not args:
    print "usage: {start|stop|status} [--url url] [--ip ip] [--port port] [--radio radio]";
    sys.exit(1)

  start = False
  status = False
  if args[0] == 'start':
    start = True
  elif args[0] == 'stop':
    start = False
  elif args[0] == 'status':
    status = True
  else: 
    print 'command {start|stop} not specified'
    sys.exit(1)
  del args[0]

  url = 'http://stream4.nadaje.com:8002/muzo'
  if args and args[0] == '--url':
    url = args[1]
    del args[0:2]
  
  ip = '192.168.0.3'
  if args and args[0] == '--ip':
    ip = args[1]
    del args[0:2]
  
  port = 6600
  if args and args[0] == '--port':
    port = num(args[1])
    del args[0:2]
  
  if args and args[0] == '--radio':
    radio = num(args[1])
    del args[0:2]
    if radio == 2:
      url = ''
  
  if status:
    print_status(ip, port)
    sys.exit(0)

  print 'Connecting to mpd server:',ip,':',port
  if start:
    print 'Playing: ', url
    play(ip, port, url)
  else:  
    print 'Stopping'
    stop(ip, port)

if __name__ == "__main__":
  main()
