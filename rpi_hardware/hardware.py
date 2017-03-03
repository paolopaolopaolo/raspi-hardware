import RPi.GPIO as GPIO

class Hardware(object):
    '''
    Hardware Base: Feed it a dictionary with Hashable keys and tuple values
    Will save pins directly to the instance as attributes prefixed by "pin_"
    '''
    debug = False

    def setup_pins(self, pin_setup):
        GPIO.setmode(GPIO.BCM)
        for element, arguments in pin_setup.items():
            args = []
            kwargs = {}

            for arg in arguments:
                if type(arg) is not dict:
                    args.append(arg)
                else:
                    kwargs = arg

            # Saves the pin as "pin_<pin name>"
            setattr(self, "pin_".format(element), arguments[0])

            # Setup the pin
            GPIO.setup(*args, **kwargs)
            if self.debug:
                print("GPIO.setup(*args={}, **kwargs={})".format(args, kwargs))

    def __init__(self, pin_setup, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.pin_setup = pin_setup
        self.setup_pins(pin_setup)


def test():
    '''
    Runs Unit Test for Pin Setup
    '''
    pin_setup = {
            'button': (11, GPIO.IN, {'pull_up_down': GPIO.PUD_UP}),
            'tiltSwitchR': (18, GPIO.IN, {'pull_up_down': GPIO.PUD_UP}),
            'tiltSwitchL': (22, GPIO.IN, {'pull_up_down': GPIO.PUD_UP}),
            'ledGreen1': (21, GPIO.OUT),
            'ledRed2': (13, GPIO.OUT),
            'ledYellow': (23, GPIO.OUT),
            'ledRed1': (19, GPIO.OUT),
            'ledGreen2': (24, GPIO.OUT)
        }

    h = Hardware(pin_setup, serial_device="TEST_OBJECT", debug=True)
    
    # Compare h.pin_button, h.pin_tiltSwitchR, etc. with what we know they should be
    pin_attributes = ["pin_{}".format(key) for key in pin_setup.keys()]
    pin_numbers = [getattr(h, attribute) for attribute in pin_attributes]

    assert (pin_numbers == [11, 18, 22, 21, 13, 23, 19, 24])

    assert (h.serial_device == "TEST_OBJECT")
    assert (h.debug == True)
    print("Tests passed!")


if __name__ == '__main__':
    # Copy paste this boilerplate over to new projects
    import sys
    if len(sys.argv) > 1:
        if 'test' in sys.argv:
            test()
        
