import RPi.GPIO as GPIO

class Hardware(object):
    '''
    Hardware Base: Feed it a dictionary with Hashable keys and tuple values and each 
    '''
    debug = False
    key_to_pin_num = {}

    def setup_pins(self, pin_setup):
        GPIO.setmode(GPIO.BCM)
        for element, arguments in pin_setup.iteritems():
            args = []
            kwargs = {}
            for arg in arguments:
                if type(arg) is not dict:
                    args.append(arg)
                else:
                    kwargs = arg    
            self.key_to_pin_num[element] = arguments[0]
            GPIO.setup(*args, **kwargs)
            if self.debug:
                print "GPIO.setup(*args={}, **kwargs={})".format(args, kwargs)
        if self.debug:
            print "key_to_pin_num:{}".format(self.key_to_pin_num)

    def __init__(self, pin_setup, **kwargs):
        for key, value in kwargs.iteritems():
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
    keys = sorted(h.key_to_pin_num.keys())
    assert(keys == ['button', 'ledGreen1', 'ledGreen2',
                    'ledRed1', 'ledRed2', 'ledYellow',
                    'tiltSwitchL', 'tiltSwitchR'])
    assert (h.serial_device == "TEST_OBJECT")
    assert (h.debug == True)
    print "Tests passed!"


if __name__ == '__main__':
    # Copy paste this boilerplate over to new projects
    import sys
    if len(sys.argv) > 1:
        if 'test' in sys.argv:
            test()
        
