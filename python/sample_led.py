#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple client for GiGA Genie AI Makers Kit"""

from __future__ import print_function
from __future__ import absolute_import

import gkit
import time

def sample():
    
    # led
    led = gkit.get_led()
    print ('led blink')
    led.set_state(gkit.LED.BLINK)
    time.sleep(5)
    print ('led beacon')
    led.set_state(gkit.LED.BEACON)
    time.sleep(15)
    print ('led decay')
    led.set_state(gkit.LED.DECAY)
    time.sleep(5)
    print ('led pulse quick')
    led.set_state(gkit.LED.PULSE_QUICK)
    time.sleep(5)
    print ('led off')
    led.set_state(gkit.LED.OFF)
    time.sleep(5)
    led.stop()

    message = input('press enter to quit\n\n')


def main():

    sample()

if __name__ == '__main__':
    main()
