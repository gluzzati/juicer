#!/usr/bin/env python

import sys

import RPi.GPIO as GPIO

from flow_meter.flowmeter import FlowMeter

fm = FlowMeter(18, 4.25)

while True:
    try:
        input("press to enable")
        fm.enable()
        tare = input("press to tare")
        fm.tare(float(tare))
        input("press to disable")
        fm.disable()
        fm.reset()

    except KeyboardInterrupt:
        print('\ncaught keyboard interrupt!, bye')
        GPIO.cleanup()
        sys.exit()
