import RPi.GPIO as GPIO
import os
from config import SERIAL_DEVICE, PIN_SETUP
from hardware import Hardware
from utils import main_loop
import serial, time

class LightSensor(Hardware):

    serial_device = None
    debug = False
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
        if self.debug:
            print "led_keys: {}".format(self.led_keys)
        while 1:
            if self.debug:
                print "{}".format(self.get_dataline())
            dataline = self.get_dataline()
            try:
                if int(dataline) < 200:
                    self.all_off() 
                    GPIO.output(self.key_to_pin_num[self.led_keys[2]], GPIO.HIGH)
                elif (int(dataline) < 500):
                    self.all_off()
                    GPIO.output(self.key_to_pin_num[self.led_keys[1]], GPIO.HIGH)
                    GPIO.output(self.key_to_pin_num[self.led_keys[2]], GPIO.HIGH)
                    GPIO.output(self.key_to_pin_num[self.led_keys[3]], GPIO.HIGH)
                else:
                    self.all_off()
                    GPIO.output(self.key_to_pin_num[self.led_keys[0]], GPIO.HIGH)
                    GPIO.output(self.key_to_pin_num[self.led_keys[1]], GPIO.HIGH)
                    GPIO.output(self.key_to_pin_num[self.led_keys[2]], GPIO.HIGH)
                    GPIO.output(self.key_to_pin_num[self.led_keys[3]], GPIO.HIGH)
                    GPIO.output(self.key_to_pin_num[self.led_keys[4]], GPIO.HIGH)
            except ValueError:
                pass
            time.sleep(0.050)

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

@main_loop
def debug():
    ls = LightSensor(PIN_SETUP, debug=True)
    ls.start()

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        if 'test' in sys.argv:
            test()
        if 'start' in sys.argv:
            start()
        if 'debug' in sys.argv:
            debug()