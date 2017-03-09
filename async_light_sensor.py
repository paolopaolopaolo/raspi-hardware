import RPi.GPIO as GPIO
import os
from config import SERIAL_DEVICE, PIN_SETUP
from rpi_hardware import Hardware, main_loop
import serial, time, datetime, functools
import json
import asyncio
import websockets
import serial_asyncio

class SerialConnection(asyncio.Protocol):

    data_buffer = ''

    async def send_data(self, data):
        async with websockets.connect(os.getenv('PUBLISH_SOCKET_LINK')) as ws:
            # Check that it's a number
            dataline = data
            if dataline != '':
                await ws.send(dataline)

    def data_received(self, data):
        self.data_buffer += data.decode('utf-8')
        if '\r\n' in self.data_buffer:
            data_to_send = self.data_buffer.strip('\r\n')
            self.data_buffer = ''
            asyncio.get_event_loop().create_task(self.send_data(data_to_send))

# @main_loop
def record(path = None):
    loop = asyncio.get_event_loop()
    serial_connection = serial_asyncio.create_serial_connection(loop, SerialConnection, SERIAL_DEVICE, baudrate=9600)
    try:
        loop.run_until_complete(serial_connection)
        loop.run_forever()
    finally:
        loop.close()

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        if 'record' in sys.argv:
            record()