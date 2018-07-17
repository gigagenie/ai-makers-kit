#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple Client for GiGA Genie AI Makers Kit"""

from __future__ import print_function
from __future__ import absolute_import

import gkit
import time
import traceback

# set your client key information on gkit.config(CONFIG FILE)

led_state = {
    'ready'     : gkit.LED.PULSE_QUICK,
    'listening' : gkit.LED.BLINK,
    'playing'   : gkit.LED.ON,
    'off'       : gkit.LED.OFF,
}
led = gkit.get_led()

def myservice():
    led.set_state(led_state['listening'])
    stt_text = gkit.getVoice2Text()

    led.set_state(led_state['playing'])
    print (stt_text)
    if stt_text != '':
        gkit.tts_play(stt_text)

    led.set_state(led_state['ready'])

def main():

    detector = gkit.KeywordDetector()
    # keyword: '지니야'(default), '기가지니', '친구야', '자기야'
    detector.setkeyword('친구야')
    try:
        led.set_state(led_state['ready'])
        detector.start(callback = myservice)
    except KeyboardInterrupt:
        detector.terminate()
        led.set_state(led_state['off'])
        time.sleep(1)
        led.stop()
    except:
        traceback.print_exc()

if __name__ == '__main__':
    main()
