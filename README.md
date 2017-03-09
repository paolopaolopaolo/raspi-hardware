# raspi-hardware
Python Classes for interacting with GPIO pins on Raspberry Pi:

The `Hardware` class enables hardware/software tinkerers on the Pi to develop projects
in a slightly more organized way. Rather than setup pins in a bunch of calls to `GPIO.setup`, you can 
list all the pins to be set up in a dictionary object. Running programs from instance methods makes projects easier 
to unit test. 

## Requirements:
- RPi.GPIO
- pyserial
- pip

## Setup:
- Installation:
```
$ git clone git@github.com:paolopaolopaolo/raspi-hardware.git // OR 'git clone https://github.com/paolopaolopaolo/raspi-hardware.git'
$ cd raspi-hardware
$ pip install --editable .
```

## Things you can do with this stuff
- Inherit from the `Hardware` class 
- Use `main_loop` decorator to wrap in `try/except` block that runs `GPIO.cleanup` after `KeyboardInterrupt`

```python
# button_press.py
from rpi_hardware import Hardware, main_loop
import RPi.GPIO as GPIO
import time

class ButtonPress(Hardware):
  '''
  Expects the PIN_SETUP to define the following:
  * "button"
  * "0_led_1"
  '''

  is_light_on = False
  
  @main_loop
  def start(self):
    while True:
      if GPIO.input(self.pin_button) == False:
        self.is_light_on = self.not is_light_on
        if self.is_light_on:
          GPIO.output(self.pin_0_led1, GPIO.HIGH)
        else:
          GPIO.output(self.pin_0_led1, GPIO.LOW)
        time.sleep(0.2)
```

- Create a PIN SETUP dictionary, and instantiate your class with it
````python
# 
import RPi.GPIO as GPIO
from .button_press import ButtonPress

PIN_SETUP = {
  "button": (18, GPIO.IN, {"pull_up_down": GPIO.PUD_UP}),
  "0_led1": (11, GPIO.OUT)
}

if __name__ == '__main__':
  button_press = ButtonPress(PIN_SETUP) # Runs GPIO.setup on each item in PIN_SETUP
  button_press.start()

````
- Look at the example projects (`light_sensors.py` and `light_tilt.py` for some more direction)
