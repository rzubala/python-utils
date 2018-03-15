#!/usr/bin/env python

import RPi.GPIO as gpio

#set up pin 14 as an input
gpio.setmode(gpio.BCM)
gpio.setup(14, gpio.IN)

while True:
  input_value = gpio.input(14)
  if input_value == False:
    print('Przycisk wcisniety...')
    while input_value == False:
      input_value = gpio.input(14)

gpio.cleanup() 
