#!/usr/bin/env python

import mpd_client
import RPi.GPIO as gpio
import time
import commands

def main_loop():
  gpio.setmode(gpio.BCM)
  gpio.setup(21, gpio.IN, pull_up_down=gpio.PUD_UP)
  
  try:
    button_down = 0  
    button_down_2 = 0  
    while True:
      button = gpio.input(21)
      if not button:
        if not button_down:
          button_down = time.time()
      else:
        now = time.time()
        if button_down:
          diff = now - button_down
          if diff < 1.0:
            play()
          elif diff > 1.0 and diff < 3.0:
            stop()  
          elif diff > 3.0 and diff < 5.0:
            network_restart()
          elif diff > 5.0 and diff < 8.0:
            restart()
          elif diff > 8.0:
            shutdown()
        button_down = 0
      time.sleep(100.0/1000.0) 

  except KeyboardInterrupt, e:
    gpio.cleanup()

def play():
  url = 'http://stream4.nadaje.com:8002/muzo'
  ip = '127.0.0.1'
  port = 6600
  print 'Connecting to mpd server:',ip,':',port
  print 'Playing: ', url
  mpd_client.play(ip, port, url)

def stop():
  ip = '127.0.0.1'
  port = 6600
  print 'Connecting to mpd server:',ip,':',port
  print 'Stoping: '
  mpd_client.stop(ip, port)
    
def network_restart():
  cmd = 'service networking restart'
  print 'network restart', cmd
  (status, output) = commands.getstatusoutput(cmd)
  if status:
    sys.stderr.write(output)
    sys.exit(status)
  print output

def restart():
  cmd = 'shutdown -r 0'
  print 'restart', cmd
  (status, output) = commands.getstatusoutput(cmd)
  if status:
    sys.stderr.write(output)
    sys.exit(status)
  print output

def shutdown():
  cmd = 'shutdown -h 0'
  print 'restart', cmd
  (status, output) = commands.getstatusoutput(cmd)
  if status:
    sys.stderr.write(output)
    sys.exit(status)
  print output
    
main_loop()
