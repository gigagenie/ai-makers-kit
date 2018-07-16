#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Simple client for GiGA Genie AI Makers Kit"""

from __future__ import print_function
from __future__ import absolute_import

import gkit

# set your client key information on gkit.config(CONFIG FILE)

def sample():
    
    gkit.kws_start()
    gkit.kws_setkeyword('기가지니')
    
    while True:
        print ('========')
        if gkit.kws_detect() == 1:
            stt_text = gkit.getVoice2Text()
            print (stt_text)
            if stt_text != '':
                gkit.tts_play(stt_text)

def main():

    sample()

if __name__ == '__main__':
    main()
