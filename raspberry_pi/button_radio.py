#!/usr/bin/env python

import mpd_client
import RPi.GPIO as gpio
import time

def main_loop():
  gpio.setmode(gpio.BCM)
  gpio.setup(14, gpio.IN)
  gpio.setup(15, gpio.OUT)
  
  try:
    button_down = 0  
    while True:
      button = gpio.input(14)
      if not button:
        gpio.output(15, gpio.HIGH)
        if not button_down:
          button_down = time.time()
      else:
        gpio.output(15, gpio.LOW)
        now = time.time()
        if button_down:
          diff = now - button_down
          if diff < 1.0:
            play()
          else:
            stop()  
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
    
main_loop()
