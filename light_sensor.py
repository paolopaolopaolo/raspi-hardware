import RPi.GPIO as GPIO
import os
from config import SERIAL_DEVICE, PIN_SETUP
from hardware import Hardware
from utils import main_loop
import serial, time, datetime

class LightSensor(Hardware):

    serial_device = None
    off = False
    debug = False
    led_keys = []

    def all_off(self):
        for led in self.led_keys:
            GPIO.output(self.key_to_pin_num[led], GPIO.LOW)

    def get_dataline(self):
        return self.serial_device.readline().strip("\r\n")

    def write_dataline_to_file(self, path):
        while 1:
            with open(path, "a") as datafile:
                datafile.write("{},{}\n".format(datetime.datetime.now(), self.get_dataline()))
            time.sleep(0.050)

    def data_to_light(dataline):
        try:
            data_int = int(dataline)
            top_key = 0
            if data_int < 50:
                top_key = 1
            elif data_int < 100:
                top_key = 2
            elif data_int < 250:
                top_key = 3
            elif data_int < 650:
                top_key = 4
            elif data_int < 850:
                top_key = 5
            elif data_int < 950:
                top_key = 6
            else:
                top_key = 7
            for key in self.led_keys[0:top_key]:
                GPIO.output(self.key_to_pin_num[key], GPIO.HIGH)
        except:
            pass

    def start(self):
        if self.debug:
            print "led_keys: {}".format(self.led_keys)
        while 1:
            if not self.off:
                if self.debug:
                    print "{}".format(self.get_dataline())
                dataline = self.get_dataline()
                try:
                    self.all_off()
                    self.data_to_light(dataline)
                except ValueError:
                    pass
                time.sleep(0.050)
            if GPIO.input(self.key_to_pin_num['button']) == False:
                self.off = not self.off
                self.all_off()
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
def record(path):
    ls = LightSensor(PIN_SETUP)
    ls.write_dataline_to_file(path)


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
        if 'record' in sys.argv:
            record(sys.argv[2])