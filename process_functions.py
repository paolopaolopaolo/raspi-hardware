import RPi.GPIO as GPIO
import time

def on_and_off(pin_output):
	GPIO.output(pin_output, GPIO.HIGH)
	time.sleep(0.5)
	GPIO.output(pin_output, GPIO.LOW)
	time.sleep(1.0)

def on_for_a_while(pin_output, seconds=5):
	print "ON"
	GPIO.output(pin_output, GPIO.HIGH)
	time.sleep(seconds)
	print "OFF"
	GPIO.output(pin_output, GPIO.LOW)

if __name__ == '__main__':
	pass