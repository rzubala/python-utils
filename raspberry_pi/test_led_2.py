#!/usr/bin/env python

import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
gpio.setup(14, gpio.OUT)
gpio.setup(15, gpio.OUT)

while True: 
  gpio.output(14, gpio.HIGH) 
  gpio.output(15, gpio.LOW) 
  time.sleep(1) 
  gpio.output(14, gpio.LOW) 
  gpio.output(15, gpio.HIGH) 
  time.sleep(1)
