#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example 5: Dialog - queryByText"""

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
	sslCred = grpc.ssl_channel_credentials()

	authCred = grpc.metadata_call_credentials(credentials)

	return grpc.composite_channel_credentials(sslCred, authCred)

### END OF COMMON ###

# DIALOG : queryByText
def queryByText(text):

	channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), getCredentials())
	stub = gigagenieRPC_pb2_grpc.GigagenieStub(channel)

	message = gigagenieRPC_pb2.reqQueryText()
	message.queryText = text
	message.userSession = "1234"
	message.deviceId = "yourdevice"
		
	response = stub.queryByText(message)

	print ("\n\nresultCd: %d" % (response.resultCd))
	if response.resultCd == 200:
		print ("\n\n\n질의한 내용: %s" % (response.uword).encode('utf-8'))
		#dssAction = response.action
		for a in response.action:
			#print (a.mesg)
			response = (a.mesg).encode('utf-8')
			#print (a.actType)
		parsing_resp = response.replace('<![CDATA[', '')
		parsing_resp = parsing_resp.replace(']]>', '')
		print("\n\n질의에 대한 답변: " + parsing_resp + '\n\n\n')
		#return response.url
	else:
		print ("Fail: %d" % (response.resultCd))
		#return None	 

def main():

	# Dialog : queryByText
	queryByText("안녕")

if __name__ == '__main__':
	main()
