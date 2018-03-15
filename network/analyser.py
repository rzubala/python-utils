#!/usr/bin/python

import sys
import re

def num(s):
  try:
    return int(s)
  except ValueError:
    return 0
  
def first(x):
  match = re.search(r'Channel: (\d+)', x)
  if match:
    return num(match.group(1))
  return x

def last(x):
  power = x[2]  
  match = re.search(r'-(\d+) dBm', power)
  if match:
    return match.group(1)  
  return power
  
def print_cells(cells):
  sorted_cells = sorted(cells, key=last)  
  for cell in sorted_cells:
    print '\t\t','\t'.join(cell)

def process_channels(channels):
  print_cells([(crop('name:', 20), crop('quality:', 10), crop('power:', 10))])
  sorted_keys = sorted(channels, key=first)
  for channel in sorted_keys:
      print channel
      print_cells(channels[channel])

def crop(name, chars):
  if len(name) > chars:  
    return name[:chars]
  else:
    return name.ljust(chars)

def main():
  channels = {}
  channel = ''
  name = ''
  quality = ''
  level = ''
  for line in sys.stdin:
    to_add = False
    match = re.search(r'Frequency:(.+) GHz \(Channel (\d+)\)', line)
    if match:
      channel = 'Channel: '+ match.group(2) + ' ('+ match.group(1)+' GHz)'
      name = ''
      quality = ''
      level = ''
    match = re.search(r'Quality=(\S+)\s+Signal level=(.+) dBm', line)
    if match:
      quality = crop(match.group(1), 10)
      level = crop(match.group(2) + ' dBm', 10)
    match = re.search(r'ESSID:"(.+)"', line)
    if match:
      name = crop(match.group(1), 20)
      to_add = True

    if to_add:
      if channel in channels:
        channels[channel].append((name, quality, level))
      else:
        channels[channel] = [(name, quality, level)]  

  process_channels(channels)
    
if __name__ == "__main__":
  main()
