#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example 3: TTS - getText2VoiceUrl"""

from __future__ import print_function

import grpc
import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc
import user_auth as UA
import os

HOST = 'gate.gigagenie.ai'
PORT = 4080


# TTS : getText2VoiceUrl
def getText2VoiceUrl(inText):

	channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), UA.getCredentials())
	stub = gigagenieRPC_pb2_grpc.GigagenieStub(channel)

	message = gigagenieRPC_pb2.reqText()
	message.lang=0
	message.mode=0
	message.text=inText
	response = stub.getText2VoiceUrl(message)

	print ("\n\nresultCd: %d" % (response.resultCd))
	if response.resultCd == 200:
		print ("TTS 생성에 성공하였습니다.\n\n\n아래 URL을 웹브라우져에 넣어보세요.")
		print ("Stream Url: %s\n\n" % (response.url))
	else:
		print ("TTS 생성에 실패하였습니다.")
		print ("Fail: %d" % (response.resultCd)) 

def main():
	getText2VoiceUrl("안녕하세요. 반갑습니다.")

if __name__ == '__main__':
	main()
