#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
"""
For documentation of the webbrowser module,
see http://docs.python.org/library/webbrowser.html
"""

'''
This application is Copyright ⓒ KT Corp. All rights reserved.

@ TITLE: YOUTUBE MOIVE PLAYER
@ Date: 2018.10.1 
@ Written by PHJ
'''

"""The Python implementation of GiGA Genie gRPC client"""
import grpc
import ex4_getText2VoiceStream as gt2vs
import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc

#Insert Selenium Libraries
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException

import os
import datetime
import hmac
import hashlib
from threading import Timer

import random
import ex2_getVoice2Text as gv2t

############
import RPi.GPIO as GPIO
GPIO.VERSION
GPIO.setmode(GPIO.BOARD)
GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(31, GPIO.OUT)
button = False

def callback(channel):	
	print("falling edge detected from pin {}".format(channel))
	global button
	button = True

GPIO.add_event_detect(29, GPIO.FALLING, callback=callback, bouncetime=10)

############
import numpy as np

# Config for GiGA Genie gRPC
CLIENT_ID = ''
CLIENT_KEY = ''
CLIENT_SECRET = ''
HOST = 'gate.gigagenie.ai' 
PORT = 4080

### Import youtube library ####
import webbrowser
import time
import os
import subprocess

import urllib.request
from bs4 import BeautifulSoup
from urllib.parse import quote

################

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

import wave

def play_file(fname):
	# create an audio object
	wf = wave.open(fname, 'rb')
	p = pyaudio.PyAudio()
	chunk = 1024

	# open stream based on the wave object which has been input.
	stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
					channels=wf.getnchannels(),
					rate=wf.getframerate(),
					output=True)

	# read data (based on the chunk size)
	data = wf.readframes(chunk)

	# play stream (looping from beginning of file to the end)
	while (data != ''):
		# writing to the stream is what *actually* plays the sound.
		stream.write(data)
		data = wf.readframes(chunk)
		#print(data)
		if data == b'':
			break
		# cleanup stuff.
	print('End of audio stream')
	stream.close()
	p.terminate()

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
				play_file("../data/sample_sound.wav")
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




######### Search Youtube Movie #############
def search_ytmov(text):
	ytmov_list = []
	gt2vs.getText2VoiceStream("검색어" + text + "해당하는 유튜브 동영상을 검색중입니다 잠시만 기다려주세요", "./yt_search.wav")
	play_file("./yt_search.wav")
	textToSearch = text
	query = quote(textToSearch)
	url = "https://www.youtube.com/results?search_sort=video_view_count&filters=video%2C+video&search_query=" + query
	response = urllib.request.urlopen(url)
	html = response.read()
	soup = BeautifulSoup(html)

	for vid in soup.findAll(attrs={'class':'yt-uix-tile-link'}):
		temp_str = ('https://www.youtube.com' + vid['href'])
		ytmov_list.append(temp_str)

	print("----------------")
	print(ytmov_list[1]) # Return the most viewed YouTube movie's url
	return ytmov_list[1]

	

#### Execute Browser ####
def exec_browser(youtube_url, title):
	already_off = 0
	gt2vs.getText2VoiceStream("가장 조회수가 많은 " + title + "의 동영상을 재생합니다.", "./yt_result.wav")
	play_file("./yt_result.wav")
	driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
	driver.maximize_window()
	driver.get(youtube_url)
	driver.switch_to.frame(0)
	player_status = driver.execute_script("return document.getElementById('movie_player').getPlayerState()")
	fullscreen_elem = driver.find_element_by_xpath("//div[@class='ytp-right-controls']/button[@class='ytp-fullscreen-button ytp-button']")
	print(player_status)
	time.sleep(3)
	fullscreen_elem.click()
	while player_status != 0:
		player_status = driver.execute_script("return document.getElementById('movie_player').getPlayerState()")
		time.sleep(2)
		text = gv2t.getVoice2Text()
		if(text == '종료'):
			already_off = 1
			driver.quit()
			gt2vs.getText2VoiceStream("유튜브 동영상 재생을 종료합니다. 감사합니다.", "./yt_end.wav")
			play_file("./yt_end.wav")
			print('Youtube movie End.')
			break
	
	if(already_off == 0):
		print('Youtube movie End.')
		driver.quit()

#### Main Function ####
def main():
	while 1:
		retry_game = True
		button = False
		recog=kws_test()
		print(recog)
		msg = '종료'
		say_exit = msg
		if recog == 200:
			time.sleep(0.8)
			while 1:
				if retry_game:
					print("Speech Recognize Start.....\n")
					gt2vs.getText2VoiceStream("검색하고자 하는 가수명을 말씀하세요.", "./say_singer.wav")
					play_file("./say_singer.wav")
					text = gv2t.getVoice2Text()
					if(text == '' or text == '종료'):
						gt2vs.getText2VoiceStream("유튜브 동영상 프로그램을 종료합니다. 감사합니다.", "./yt_end.wav")
						play_file("./yt_end.wav")
						
						break

					if(say_exit in text):
						break
					target_url = search_ytmov(text) #searching youtube movie
					exec_browser(target_url, text)	#Playing most viewed youtube music video
					time.sleep(2)
		else:
			print('Not_play_now ...')

if __name__ == '__main__':
	main()
