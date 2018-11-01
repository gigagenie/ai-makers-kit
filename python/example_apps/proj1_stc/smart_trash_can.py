#!/usr/bin/env python
# -*- coding: utf-8 -*-


""" This application is Copyright ⓒ KT Corp. All rights reserved. """

"""The Python implementation of GiGA Genie gRPC client"""

from __future__ import print_function
import grpc
import PCA9685 as servo		# Import Servo Motor Driver
import time                # Import necessary modules

import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc

import os
import datetime
import hmac
import hashlib
from threading import Timer

############
import RPi.GPIO as GPIO
GPIO.VERSION
GPIO.setmode(GPIO.BOARD)
#GPIO.setup(29, GPIO.IN)
GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(31, GPIO.OUT)
button = False

'''
Smart Trash Can Functions
(스마트 휴지통 서보 모터 컨트롤 함수)
setup: 초기 서보모터 각도 설정
open_tc: 휴지통을 여는 함수
close_tc: 휴지통을 닫는 함수
'''
###############################################
def setup(busnum=None):
	global openPWM, homePWM, pwm
	openPWM = 420
	homePWM = 700
	offset =0
	try:
		for line in open('config'):
			if line[0:8] == 'offset =':
				offset = int(line[9:-1])
	except:
		print("config error")
	openPWM += offset
	homePWM += offset
	if busnum == None:
		pwm = servo.PWM()                  # Initialize the servo controller.
	else:
		pwm = servo.PWM(bus_number=busnum) # Initialize the servo controller.
	pwm.frequency = 60

def open_tc():
	global openPWM
	pwm.write(0, 0, openPWM)  # CH0

def close_tc():
	global homePWM
	pwm.write(0, 0, homePWM)
################################################


def callback(channel):
	print("falling edge detected from pin {}".format(channel))
	global button
	button = True

GPIO.add_event_detect(29, GPIO.FALLING, callback=callback, bouncetime=10)

############
import numpy as np
import ex2_getVoice2Text as gv2t
import ex4_getText2VoiceStream as gt2vt

# Config for GiGA Genie gRPC
CLIENT_ID = ''
CLIENT_KEY = ''
CLIENT_SECRET = ''
HOST = 'gate.gigagenie.ai' 
PORT = 4080 

### COMMON : Client Credentials ###
def getMetadata():
	timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
	message = CLIENT_ID + ':' + timestamp

	signature = hmac.new(CLIENT_SECRET, message, hashlib.sha256).hexdigest()

	metadata = [('x-auth-clientkey', CLIENT_KEY),
				('x-auth-timestamp', timestamp),
				('x-auth-signature', signature)]

	return metadata

def credentials(context, callback):
	callback(getMetadata(), None)

def getCredentials():
	with open('../data/ca-bundle.pem', 'rb') as f:
		trusted_certs = f.read()
	sslCred = grpc.ssl_channel_credentials(root_certificates=trusted_certs)

	authCred = grpc.metadata_call_credentials(credentials)

	return grpc.composite_channel_credentials(sslCred, authCred)

### KWS
import pyaudio
import audioop
from six.moves import queue

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 512

# MicrophoneStream - original code in https://goo.gl/7Xy3TT
class MicrophoneStream(object):
	"""Opens a recording stream as a generator yielding the audio chunks."""
	def __init__(self, rate, chunk):
		self._rate = rate
		self._chunk = chunk

		# Create a thread-safe buffer of audio data
		self._buff = queue.Queue()
		self.closed = True

	def __enter__(self):
		self._audio_interface = pyaudio.PyAudio()
		self._audio_stream = self._audio_interface.open(
			format=pyaudio.paInt16,
			channels=1, rate=self._rate,
			input=True, frames_per_buffer=self._chunk,
			# Run the audio stream asynchronously to fill the buffer object.
			# This is necessary so that the input device's buffer doesn't
			# overflow while the calling thread makes network requests, etc.
			stream_callback=self._fill_buffer,
		)

		self.closed = False

		return self

	#def __exit__(self, type, value, traceback):
	def __exit__(self, type, value, traceback):		
		self._audio_stream.stop_stream()
		self._audio_stream.close()
		self.closed = True
		# Signal the generator to terminate so that the client's
		# streaming_recognize method will not block the process termination.
		self._buff.put(None)
		self._audio_interface.terminate()
	
	def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
		"""Continuously collect data from the audio stream, into the buffer."""
		self._buff.put(in_data)
		return None, pyaudio.paContinue

	def generator(self):
		while not self.closed:
			# Use a blocking get() to ensure there's at least one chunk of
			# data, and stop iteration if the chunk is None, indicating the
			# end of the audio stream.
			chunk = self._buff.get()
			if chunk is None:
				return
			data = [chunk]

			# Now consume whatever other data's still buffered.
			while True:
				try:
					chunk = self._buff.get(block=False)
					if chunk is None:
						return
					data.append(chunk)
				except queue.Empty:
					break

			yield b''.join(data)
# [END audio_stream]

def print_rms(rms):
	out = ''
	for _ in xrange(int(round(rms/30))):
		out = out + '*'
	
	print (out)

# KWS

import ktkws
KWSID = ['기가지니', '지니야', '친구야', '자기야']

def detect():
	global button
	with MicrophoneStream(RATE, CHUNK) as stream:
		audio_generator = stream.generator()

		for content in audio_generator:
			#import binascii
			#print ("INBYTE: %s" % (binascii.hexlify(bytearray(content))))
			GPIO.output(31, GPIO.HIGH)
			rc = ktkws.detect(content)
			rms = audioop.rms(content,2)
			#print('audio rms = %d' % (rms))
			GPIO.output(31, GPIO.LOW)
			if (button == True):
				rc = 1
				button = False
			
			if (rc == 1):
				GPIO.output(31, GPIO.HIGH)
				gt2vt.play_file("../data/sample_sound.wav")
				return 200

def kws_test():
	rc = ktkws.init("../data/kwsmodel.pack")
	print ('init rc = %d' % (rc))
	rc = ktkws.start()
	#print ('start rc = %d' % (rc))
	ktkws.set_keyword(KWSID.index('기가지니'))
	rc = detect()
	print ('detect rc = %d' % (rc))
	ktkws.stop()
	ktkws.reset()
	return rc

def control_action(text):
	open_can = '열어'.decode('utf-8')
	open_can2 = '열어줘'.decode('utf-8')
	open_can3 = '여러'.decode('utf-8')
	close_can = '닫아'.decode('utf-8')
	close_can2 = '닫아줘'.decode('utf-8')
	#cmd_init()
	
	if (open_can in text or open_can2 in text):
		print('open the trash can')
		gt2vt.getText2VoiceStream("네에","./stc_yes.wav")
		gt2vt.play_file("./stc_yes.wav")
		time.sleep(1)
		open_tc()
		time.sleep(3)
	elif (close_can in text or close_can2 in text):
		print('close the trash can')
		gt2vt.getText2VoiceStream("네에","./stc_yes.wav")
		gt2vt.play_file("./stc_yes.wav")
		close_tc()
	else:
		print('action nothing')

def main():
	setup()
	while 1:
		retry_game = True
		button = False
		recog=kws_test()
		say_exit = '종료'.decode('utf-8')
		if recog == 200:
			gt2vt.getText2VoiceStream("안녕하세요 영리한 휴지통입니다","./stc_opening.wav")
			gt2vt.play_file("./stc_opening.wav")
			time.sleep(0.8)
			while 1:
				if retry_game:
					text = gv2t.getVoice2Text()
					control_action(text)
					if(say_exit in text):
						gt2vt.getText2VoiceStream("감사합니다","./stc_thanku.wav")
						gt2vt.play_file("./stc_opening.wav")
						break
		else:
			print('Not play now ...')

if __name__ == '__main__':
	main()
