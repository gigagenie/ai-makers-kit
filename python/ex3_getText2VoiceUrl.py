#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The Python implementation of GiGA Genie gRPC client"""

from __future__ import print_function

import grpc

import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc

import os
import datetime
import hmac
import hashlib

# Config for GiGA Genie gRPC
CLIENT_ID = '10000036'
CLIENT_KEY = 'AIY_HELLO_KEY_10000036'
CLIENT_SECRET = 'AIY_HELLO_SECRET_10000036'
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

    print ("resultCd: %d" % (response.resultCd))
    if response.resultCd == 200:
        print ("Stream Url: %s" % (response.url))
    else:
        print ("Fail: %d" % (response.resultCd)) 

def main():
    getText2VoiceUrl("안녕하세요. 반갑습니다.")

if __name__ == '__main__':
    main()
