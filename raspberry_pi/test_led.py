#!/usr/bin/env python

import RPi.GPIO as gpio
import time

#set up pin 14 as an output
gpio.setmode(gpio.BCM)
gpio.setup(14, gpio.OUT)

gpio.output(14, gpio.HIGH)
time.sleep(3)
gpio.output(14, gpio.LOW)

gpio.cleanup()
