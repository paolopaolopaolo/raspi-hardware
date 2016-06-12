import RPi.GPIO as GPIO
# Configuration settings

PIN_SETUP = {
    'button': (11, GPIO.IN, {'pull_up_down': GPIO.PUD_UP}),
    'tiltSwitchL': (18, GPIO.IN, {'pull_up_down': GPIO.PUD_UP}),
    'tiltSwitchR': (22, GPIO.IN, {'pull_up_down': GPIO.PUD_UP}),
    '2_ledGreen1': (21, GPIO.OUT),
    '5_ledRed2': (13, GPIO.OUT),
    '3_ledYellow1': (23, GPIO.OUT),
    '6_ledYellow2': (14, GPIO.OUT),
    '1_ledRed1': (19, GPIO.OUT),
    '4_ledGreen2': (24, GPIO.OUT),
    '0_ledYellow0': (15, GPIO.OUT)
}

SERIAL_DEVICE = '/dev/ttyACM0'
