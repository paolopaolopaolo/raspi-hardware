import RPi.GPIO as GPIO
import os
from config import SERIAL_DEVICE, PIN_SETUP
from hardware import Hardware
from utils import main_loop
import serial, time

class LightSensor(Hardware):

	serial_device = None
	led_keys = []

	def all_off(self):
		for led in self.led_keys:
			GPIO.output(self.key_to_pin_num[led], GPIO.LOW)

	def get_dataline(self):
		return self.serial_device.readline().strip("\r\n")

	def write_dataline_to_file(self, filename):
		with open("/home/pi/data/datafile.txt", "a") as datafile:
				datafile.write("\n" + self.get_dataline())

	def start(self):
		while 1:
			dataline = self.get_dataline()
			print "dataline {}".format(dataline)
			if int(dataline) > 33:
				self.all_off()
				GPIO.output(self.key_to_pin_num['1_ledGreen1'], GPIO.HIGH)
				GPIO.output(self.key_to_pin_num['3_ledGreen2'], GPIO.HIGH)
			elif int(dataline) > 66:
				self.all_off()
				GPIO.output(self.key_to_pin_num['1_ledGreen1'], GPIO.HIGH)
				GPIO.output(self.key_to_pin_num['3_ledGreen2'], GPIO.HIGH)
				GPIO.output(self.key_to_pin_num['0_ledRed1'], GPIO.HIGH)
				GPIO.output(self.key_to_pin_num['4_ledRed2'], GPIO.HIGH)
			else:
				self.all_off()
			GPIO.output(self.key_to_pin_num['2_ledYellow'], GPIO.HIGH)

			time.sleep(0.2)

	def __init__(self, *args, **kwargs):
		super(LightSensor, self).__init__(*args, **kwargs)
		self.serial_device = serial.Serial(baudrate=9600, port=SERIAL_DEVICE)
		for key in args[0].keys():
			if "led" in key:
				self.led_keys.append(key)
		self.led_keys = sorted(self.led_keys)

def test():
	ls = LightSensor({})
	assert(isinstance(ls.serial_device, serial.Serial))
	assert("\r\n" in ls.serial_device.readline())
	print "Tests passed (current value: {})!".format(ls.serial_device.readline().rstrip('\r\n'))

@main_loop
def start():
	ls = LightSensor(PIN_SETUP)
	ls.start()

if __name__ == '__main__':
	import sys
	if len(sys.argv) > 1:
		if 'test' in sys.argv:
			test()
		if 'start' in sys.argv:
			start()