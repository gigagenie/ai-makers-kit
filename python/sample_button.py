#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple client for GiGA Genie AI Makers Kit"""

from __future__ import print_function
from __future__ import absolute_import

import gkit
import time

# set your client key information
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_KEY = 'YOUR_CLIENT_KEY'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'

def onButtonHandler():
    print ("Button was pushed")
    stt_text = gkit.getVoice2Text()
    print (stt_text)
    if stt_text != '':
        gkit.tts_play(stt_text)

def sample():
    
    gkit.set_clientkey(CLIENT_ID, CLIENT_KEY, CLIENT_SECRET)

    # button
    gkit.get_button().on_press(onButtonHandler)

    message = input("Press enter to quit\n\n")
    
    #GPIO.cleanup()

def main():

    sample()

if __name__ == '__main__':
    main()
