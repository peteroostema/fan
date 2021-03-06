#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import RPi.GPIO as GPIO

import time
import subprocess
import Adafruit_MCP9808.MCP9808 as MCP9808

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
#GPIO.output(4, GPIO.LOW)

# Default constructor will use the default I2C address (0x18) and pick a default I2C bus.
#
# For the Raspberry Pi this means you should hook up to the only exposed I2C bus
# from the main GPIO header and the library will figure out the bus number based
# on the Pi's revision.
sensor = MCP9808.MCP9808()

# Optionally you can override the address and/or bus number:
#sensor = MCP9808.MCP9808(address=0x20, busnum=2)

# Initialize communication with the sensor.
tries = 10
error = None
result = None

while tries:
	try:
		sensor.begin()
	except IOError as e:
		subprocess.call(['i2cdetect', '-y', '1'])
		error = e
		tries -= 1
	else:
		break

	if not tries:
		raise error

# Loop printing measurements every second.
count = 0;
level = 0;
print('Press Ctrl-C to quit.')
while True:
	if (count == 0):
		temp = sensor.readTempC()
		print('Temperature: {0:0.3F}*C'.format(temp))
		if (temp > 24):
			level = (temp - 24) / 0.04
		print('level: ', level)
	if (level > count):
		GPIO.output(18, 1)
    	else:
        	GPIO.output(18, 0)
	if (count < 100):
		count += 1
	else:
		count = 0;
	time.sleep(0.01)


#while True:
#
#    if (GPIO.input(18) == 1):
#        print("input high")
#    else:
#        print("input low")
