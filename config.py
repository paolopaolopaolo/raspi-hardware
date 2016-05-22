import RPi.GPIO as GPIO
# Configuration settings

PIN_SETUP = {
	'button': (11, GPIO.IN, {'pull_up_down': GPIO.PUD_UP}),
	'tiltSwitchR': (18, GPIO.IN, {'pull_up_down': GPIO.PUD_UP}),
	'tiltSwitchL': (22, GPIO.IN, {'pull_up_down': GPIO.PUD_UP}),
	'1_ledGreen1': (21, GPIO.OUT),
	'4_ledRed2': (13, GPIO.OUT),
	'2_ledYellow': (23, GPIO.OUT),
	'0_ledRed1': (19, GPIO.OUT),
	'3_ledGreen2': (24, GPIO.OUT)
}

SERIAL_DEVICE = '/dev/ttyACM0'
