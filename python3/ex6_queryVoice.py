#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example 6: STT + Dialog - queryByVoice"""

from __future__ import print_function

import grpc
import time
import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc
import MicrophoneStream as MS
import user_auth as UA
import os
### STT

import audioop
from ctypes import *

RATE = 16000
CHUNK = 512

HOST = 'gate.gigagenie.ai'
PORT = 4080

ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
  dummy_var = 0
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
asound = cdll.LoadLibrary('libasound.so')
asound.snd_lib_error_set_handler(c_error_handler)

def generate_request():
	with MS.MicrophoneStream(RATE, CHUNK) as stream:
		audio_generator = stream.generator()
		messageReq = gigagenieRPC_pb2.reqQueryVoice()
		messageReq.reqOptions.lang=0
		messageReq.reqOptions.userSession="1234"
		messageReq.reqOptions.deviceId="aklsjdnalksd"
		yield messageReq
		for content in audio_generator:
			message = gigagenieRPC_pb2.reqQueryVoice()
			message.audioContent = content
			yield message
			rms = audioop.rms(content,2)

def queryByVoice():
	print ("\n\n\n질의할 내용을 말씀해 보세요.\n\n듣고 있는 중......\n")
	channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), UA.getCredentials())
	stub = gigagenieRPC_pb2_grpc.GigagenieStub(channel)
	request = generate_request()
	resultText = ''
	response = stub.queryByVoice(request)
	if response.resultCd == 200:
		print("질의 내용: %s" % (response.uword))
		for a in response.action:
			response = a.mesg
			parsing_resp = response.replace('<![CDATA[', '')
			parsing_resp = parsing_resp.replace(']]>', '')
			resultText = parsing_resp
			print("\n질의에 대한 답변: " + parsing_resp +'\n\n\n')

	else:
		print("\n\nresultCd: %d\n" % (response.resultCd))
		print("정상적인 음성인식이 되지 않았습니다.")
	return resultText

def main():
	queryByVoice()
	time.sleep(0.5)

if __name__ == '__main__':
	main()
