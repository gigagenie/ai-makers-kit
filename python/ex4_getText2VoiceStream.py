#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example 4: TTS - getText2VoiceStream"""

from __future__ import print_function

import grpc

import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc

import os
import datetime
import hmac
import hashlib
import ex1_kwstest as kws

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

# TTS : getText2VoiceStream
def getText2VoiceStream(inText,inFileName):

	channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), getCredentials())
	stub = gigagenieRPC_pb2_grpc.GigagenieStub(channel)

	message = gigagenieRPC_pb2.reqText()
	message.lang=0
	message.mode=0
	message.text=inText
	writeFile=open(inFileName,'wb')
	for response in stub.getText2VoiceStream(message):
		if response.HasField("resOptions"):
			print ("\n\nResVoiceResult: %d" %(response.resOptions.resultCd))
		if response.HasField("audioContent"):
			print ("Audio Stream\n\n")
			writeFile.write(response.audioContent)
	writeFile.close()
	return response.resOptions.resultCd

def main():
	output_file = "testtts.wav"
	getText2VoiceStream("안녕하세요. 반갑습니다.", output_file)
	kws.play_file(output_file)
	print( output_file + "이 생성되었으니 파일을 확인바랍니다. \n\n\n")
	

if __name__ == '__main__':
	main()
