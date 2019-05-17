#!/usr/bin/env python3

import RPi.GPIO as GPIO
from mfrc522.mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

while True:
	try:
       		id = reader.read_id()
        	print(id)
	finally:
		GPIO.cleanup()
