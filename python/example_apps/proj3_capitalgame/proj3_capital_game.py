#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The Python implementation of GiGA Genie gRPC client"""

from __future__ import print_function
import grpc
import time				   # Import necessary modules

import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc

import os
import re, random
import datetime
import hmac
import hashlib
from threading import Timer

############
import RPi.GPIO as GPIO
GPIO.VERSION
GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(31, GPIO.OUT)
button = False
############

wc_dict = dict()


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

def make_dict():
	global wc_dict
	with open('country_capital.txt', 'rt', encoding='utf-8') as f:
		lines = f.readlines()
	for line in lines:
		delim_index = line.find('-')
		country = line[:delim_index-1]
		capital = line[(delim_index + 2):-1]
		wc_dict.setdefault(country, capital)

def find_capital_quiz():
	global wc_dict
	num_country = len(wc_dict)
	comment_exit = '종료'
	
	
	for i in range(num_country):
		country, capital = random.choice(list(wc_dict.items()))
		print(country + "는 어디에 수도인가?")
		gt2vt.getText2VoiceStream(country + "는 어디에 수도입니까?", "./question.wav")
		gt2vt.play_file("./question.wav")
		
		text = gv2t.getVoice2Text()
		print(text + '\n')
		if (comment_exit in text):
			gameover = True	
			break
		elif (wc_dict[country] == text):
			print("정답입니다.")
			gt2vt.getText2VoiceStream("정답입니다.", "./right_answer.wav")
			gt2vt.play_file("./right_answer.wav")
			time.sleep(2)
		elif text =="":
			print("아직 답변을 듣지 못하였습니다. 3초의 시간을 더 드립니다.")
			gt2vt.getText2VoiceStream("아직 답변을 듣지 못하였습니다. 3초의 시간을 더 드립니다.", "./waits_3sec.wav")
			gt2vt.play_file("./waits_3sec.wav")
			gt2vt.getText2VoiceStream("3초", "./cn_sec.wav")
			gt2vt.play_file("./cn_sec.wav")
			time.sleep(0.8)
			gt2vt.getText2VoiceStream("2초", "./cn_sec.wav")
			gt2vt.play_file("./cn_sec.wav")
			time.sleep(0.8)
			gt2vt.getText2VoiceStream("1초", "./cn_sec.wav")
			gt2vt.play_file("./cn_sec.wav")
			time.sleep(0.8)
			gt2vt.getText2VoiceStream("이제 말씀하세요", "./say_answer.wav")
			gt2vt.play_file("./say_answer.wav")
			
			text2 = gv2t.getVoice2Text()		
			if (wc_dict[country] == text2):
				print("정답입니다.")
				gt2vt.getText2VoiceStream("정답입니다.", "./right_answer.wav")
				gt2vt.play_file("./right_answer.wav")
				time.sleep(3)
			else:
				print("오답입니다.")
				gt2vt.getText2VoiceStream("틀렸습니다. 정답은 " + country + "의 수도는 " + capital + "입니다.", "./wrong_answer.wav")
				gt2vt.play_file("./wrong_answer.wav")
				time.sleep(3)
		
		else:
			print("오답입니다.")
			gt2vt.getText2VoiceStream("틀렸습니다. 정답은 " + country + "의 수도는 " + capital + "입니다.", "./wrong_answer.wav")
			gt2vt.play_file("./wrong_answer.wav")
			time.sleep(3)
			
		del wc_dict[country]
		gt2vt.getText2VoiceStream("다음 문제를 진행하도록 하겠습니다.", "./next_quiz.wav")
		gt2vt.play_file("./next_quiz.wav")
	
	if gameover == True:
		make_dict()
		gt2vt.getText2VoiceStream("게임을 종료합니다.", "./game_end.wav")
		gt2vt.play_file("./game_end.wav")	


def main():
	global wc_dict
	make_dict()
	#find_capital_quiz()

	while 1:
		retry_game = True
		button = False
		recog=kws_test()
		say_exit = '종료'
		say_retry = '재실행'
		say_retry2 = '네'
		say_retry3 = '그래'
		
		if recog == 200:
			gt2vt.getText2VoiceStream("지금부터 나라수도 맞추기 게임을 시작합니다. 게임 중지를 원하시면 종료라고 말씀해 주세요.","./cc_opening.wav")
			gt2vt.play_file("./cc_opening.wav")
			time.sleep(0.8)
			while 1:
				if retry_game:
					find_capital_quiz()
					gt2vt.getText2VoiceStream("나라수도 맞추기 게임을 다시 시작할까요?","./stc_thanku.wav")
					gt2vt.play_file("./stc_thanku.wav")
					text = gv2t.getVoice2Text()
					if(say_exit in text):
						print("게임을 종료합니다.")
						gt2vt.getText2VoiceStream("감사합니다","./thanku.wav")
						gt2vt.play_file("./stc_thanku.wav")
						break
					elif(say_retry in text or say_retry2 in text or say_retry3 in text):
						gt2vt.getText2VoiceStream("나라수도 맞추기 게임을 다시 시작합니다.","./cc_regame.wav")
						gt2vt.play_file("./cc_regame.wav")
						retry_game = True
					else:
						gt2vt.getText2VoiceStream("감사합니다","./thanku.wav")
						gt2vt.play_file("./thanku.wav")
						break
		else:
			print('Not play now ...')


if __name__ == '__main__':
	main()
