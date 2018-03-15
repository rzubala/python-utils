#!/usr/bin/env python

import RPi.GPIO as gpio
import time

#set up pin 15 as an output and 14 as input
gpio.setmode(gpio.BCM)
gpio.setup(15, gpio.OUT)
gpio.setup(14, gpio.IN)

while True:
  input_value = gpio.input(14)
  if input_value == False:
    gpio.output(15, gpio.HIGH)
    time.sleep(1)
    gpio.output(15, gpio.LOW)
    while input_value == False:
      input_value = gpio.input(14)

gpio.cleanup()
