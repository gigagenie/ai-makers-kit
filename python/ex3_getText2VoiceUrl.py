#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example 3: TTS - getText2VoiceUrl"""

from __future__ import print_function

import grpc

import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc

import os
import datetime
import hmac
import hashlib

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
	signature = hmac.new(CLIENT_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
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

### END OF COMMON ###

# TTS : getText2VoiceUrl
def getText2VoiceUrl(inText):

	channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), getCredentials())
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
