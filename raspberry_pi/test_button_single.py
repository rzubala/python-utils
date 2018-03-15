#!/usr/bin/env python

import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
gpio.setup(21, gpio.IN, pull_up_down=gpio.PUD_UP)

try:
  while True:
    input_state = gpio.input(21)
    if input_state == False:
      print('Button Pressed')
      time.sleep(0.2)
except KeyboardInterrupt, e:
  gpio.cleanup()
