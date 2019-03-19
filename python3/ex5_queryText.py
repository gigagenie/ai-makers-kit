#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example 5: Dialog - queryByText"""

from __future__ import print_function

import grpc
import user_auth as UA
import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc
import os

HOST = 'gate.gigagenie.ai'
PORT = 4080

# DIALOG : queryByText
def queryByText(text):

	channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), UA.getCredentials())
	stub = gigagenieRPC_pb2_grpc.GigagenieStub(channel)

	message = gigagenieRPC_pb2.reqQueryText()
	message.queryText = text
	message.userSession = "1234"
	message.deviceId = "yourdevice"
		
	response = stub.queryByText(message)

	print ("\n\nresultCd: %d" % (response.resultCd))
	if response.resultCd == 200:
		print ("\n\n\n질의한 내용: %s" % (response.uword))
		#dssAction = response.action
		for a in response.action:
			response = a.mesg
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
