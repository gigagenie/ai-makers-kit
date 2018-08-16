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
    with open('../data/ca-bundle.pem', 'rb') as f:
        trusted_certs = f.read()
    sslCred = grpc.ssl_channel_credentials(root_certificates=trusted_certs)

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

    print ("resultCd: %d" % (response.resultCd))
    if response.resultCd == 200:
        print ("uword: %s" % (response.uword))
        #dssAction = response.action
        for a in response.action:
            print (a.mesg)
            print (a.actType)

        #return response.url
    else:
        print ("Fail: %d" % (response.resultCd))
        #return None	 

def main():

    # Dialog : queryByText
    queryByText("안녕")

if __name__ == '__main__':
    main()
