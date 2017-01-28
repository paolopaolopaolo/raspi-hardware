import RPi.GPIO as GPIO
import os
from config import SERIAL_DEVICE, PIN_SETUP
from hardware import Hardware
from utils import main_loop
import serial, time, datetime
import json
import asyncio
import aiohttp
import requests

class LightSensor(Hardware):
    event_loop = None
    serial_device = None
    off = False
    debug = False
    led_keys = []

    def all_off(self):
        for led in self.led_keys:
            GPIO.output(self.key_to_pin_num[led], GPIO.LOW)

    def get_dataline(self):
        return self.serial_device.readline().decode('utf-8').strip("\r\n")

    def write_dataline_to_file(self, path):
        while 1:
            with open(path, "a") as datafile:
                datafile.write("{},{}\n".format(datetime.datetime.now(), self.get_dataline()))
            time.sleep(0.050)

    async def _send_data(self, headers):
        dataline = self.get_dataline()
        new_post = {'timestamp': datetime.datetime.now().isoformat(), 'light_level': dataline}
        # Start up another of this co-routine before sending the request
        asyncio.ensure_future(self._send_data(headers))
        with aiohttp.ClientSession() as session:
            async with session.post(os.getenv('LIGHT_URL', ''), data=new_post, headers=headers) as resp:
                print('Send Success! {}'.format(datetime.datetime.now()))
                pass

    def send_data_to_server(self, future=None):
        user = os.getenv('SENSOR_USER', '')
        password = os.getenv('PASSWORD', '')
        response = requests.post(os.getenv('TOKEN_URL', ''),
                                 json={'username':user, 'password':password})
        token = json.loads(response.text).get('token', None)
        headers = {'Authorization': 'Token {}'.format(token)}
        print("Connected: {}".format(token))
        asyncio.ensure_future(self._send_data(headers))
        # Blocking call
        self.event_loop.run_forever()

    def data_to_light(self, dataline):
        try:
            data_int = int(dataline)
            top_key = 0
            if data_int < 10:
                top_key = 0
            elif data_int < 50:
                top_key = 1
            elif data_int < 230:
                top_key = 2
            elif data_int < 630:
                top_key = 3
            elif data_int < 830:
                top_key = 4
            elif data_int < 930:
                top_key = 5
            elif data_int < 980:
                top_key = 6
            else:
                top_key = 7

            if top_key == 0:
                self.all_off()
            else:
                for key in self.led_keys[0:top_key]:
                    GPIO.output(self.key_to_pin_num[key], GPIO.HIGH)
        except:
            pass

    def start(self):
        if self.debug:
            print("led_keys: {}".format(self.led_keys))
        while 1:
            if not self.off:
                if self.debug:
                    print("{}".format(self.get_dataline()))
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
        self.event_loop = asyncio.get_event_loop()
        for key in args[0].keys():
            if "led" in key:
                self.led_keys.append(key)
        self.led_keys = sorted(self.led_keys)

def test():
    ls = LightSensor({})
    assert(isinstance(ls.serial_device, serial.Serial))
    assert("\r\n" in ls.serial_device.readline().decode('utf-8'))
    print("Tests passed (current value: {})!".format(ls.serial_device.readline().decode('utf-8').rstrip('\r\n')))

@main_loop
def record(path = None):
    ls = LightSensor(PIN_SETUP)
    if path:
        ls.write_dataline_to_file(path)
    else:
        ls.send_data_to_server()

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
            if len(sys.argv) > 2:
                record(sys.argv[2])
            else:
                record()