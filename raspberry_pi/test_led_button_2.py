#!/usr/bin/env python

import RPi.GPIO as gpio
import time

#set up pin 15 as an output and 14 as input
gpio.setmode(gpio.BCM)
gpio.setup(15, gpio.OUT)
gpio.setup(14, gpio.IN)

try:
  while True:
    input_value = gpio.input(14)
    if input_value == False:
      gpio.output(15, gpio.HIGH)
    else:
      gpio.output(15, gpio.LOW)
except KeyboardInterrupt, e:
  gpio.cleanup()
