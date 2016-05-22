import RPi.GPIO as GPIO
import time
from random import randrange
from config import PIN_SETUP
from utils import next_index, prev_index, random_next_index, main_loop
from hardware import Hardware


class LightTilt(Hardware):

	ignore_switch = False
	led_index = 0
	led_keys = []
	debug = False

	def initial_state(self):
		self.all_off()

	def all_off(self):
		for led in self.led_keys:
			GPIO.output(self.key_to_pin_num[led], GPIO.LOW)

	def go_to_light(self, arg):
		if type(arg) is int:
			self.led_index = arg
		else:
			self.led_index = arg(self.led_index, self.led_keys)
		if self.debug:
			print("self.led_index={}".format(self.led_index))
		self.all_off()
		GPIO.output(self.key_to_pin_num[self.led_keys[self.led_index]], GPIO.HIGH)	

	def start(self):
		while True:
			if not GPIO.input(self.key_to_pin_num['tiltSwitchR']) and not self.ignore_switch:
				self.go_to_light(prev_index)
				time.sleep(0.01)
			if not GPIO.input(self.key_to_pin_num['tiltSwitchL']) and not self.ignore_switch:
				self.go_to_light(next_index)
				time.sleep(0.01)
			if not GPIO.input(self.key_to_pin_num['button']):
				self.ignore_switch = not self.ignore_switch
				if self.ignore_switch:
					self.initial_state()
			time.sleep(0.20)

	def __init__(self, *args, **kwargs):
		super(LightTilt, self).__init__(*args, **kwargs)
		for key in args[0].keys():
			if "led" in key:
				self.led_keys.append(key)
		self.led_keys = sorted(self.led_keys)

def test():
	t = LightTilt(PIN_SETUP)
	assert(sorted(t.led_keys) == sorted(['0_ledRed1', '1_ledGreen1', '2_ledYellow', '3_ledGreen2', '4_ledRed2']))
	assert (t.led_index == 0)
	assert (next_index(t.led_index, t.led_keys) == 1)
	print "Tests passed!"
	GPIO.cleanup()

@main_loop
def start():
	light_tilt = LightTilt(PIN_SETUP)
	light_tilt.start()


if __name__ == "__main__":
	import sys
	if len(sys.argv) > 1:
		if 'test' in sys.argv:
			test()
		if 'start' in sys.argv:
			start()
	else:
		start()