# -*- coding: utf-8 -*-

"""The Python implementation of GiGA Genie AI Makers Kit"""
# author: CheolMin Lee

from __future__ import print_function
from __future__ import absolute_import

import ktkws
from gkit._audio import *
from gkit._drivers import *
#from gkit._drivers import *

import time

KWSID = ['기가지니', '지니야', '친구야', '자기야']
KWSMODELDATA = "../data/kwsmodel.pack"
KWSSOUNDFILE = "../data/sample_yes.wav"

g_kwsid = 1     # default: 지니야

def kws_start():
    rc = ktkws.init(KWSMODELDATA)
    rc = ktkws.start()
    ktkws.set_keyword(g_kwsid)
    
    return rc

def kws_stop():
    ktkws.stop()

def kws_reset():
    ktkws.reset()
    
def kws_setkeyword(wakeword):
    global g_kwsid
    g_kwsid = KWSID.index(wakeword)
    ktkws.set_keyword(g_kwsid)

def kws_detect():

    print ('To start, say \"%s\"' % (KWSID[g_kwsid]))

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()

        for content in audio_generator:

            rc = ktkws.detect(content)
            rms = audioop.rms(content,2)
            #print('audio rms = %d' % (rms))

            if (rc == 1):
                play_wav(KWSSOUNDFILE)
                return rc

class KeywordDetector(object):

    def __init__(self):

        #ktkws.init(KWSMODELDATA)
        #ktkws.start()
        #ktkws.set_keyword(g_kwsid)
        kws_start()

        self._callback = None
        self._running = True
        self._button_pressed = False

    def _detect(self):

        print ('To start, say \"%s\" or press the button. '
               'Press Ctrl+C to quit...' % (KWSID[g_kwsid]))

        with MicrophoneStream(RATE, CHUNK) as stream:
            audio_generator = stream.generator()

            for content in audio_generator:

                rc = ktkws.detect(content)

                if (rc == 1):
                    play_wav(KWSSOUNDFILE)
                    return True
                if self._button_pressed is True:
                    return True

    def _button_callback(self):
        self._button_pressed = True

    def start(self, callback):

        self._callback = callback

        get_button().on_press(self._button_callback)

        while self._running is True:
            if self._detect() is True:
                if self._callback is not None:
                    self._callback()
                self._button_pressed = False

    def stop(self):
        self._running = False

    def terminate(self):
        kws_stop()
        self._running = False

    def setkeyword(self, wakeword):
        kws_setkeyword(wakeword)
