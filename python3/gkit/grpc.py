# -*- coding: utf-8 -*-

"""The Python implementation of GiGA Genie AI Makers Kit"""
# author: CheolMin Lee

from __future__ import print_function
from __future__ import absolute_import

from gkit._config import *
from gkit._audio import *

# gRPC
import grpc
import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc

import datetime
import hmac
import hashlib

# Config for GiGA Genie gRPC : config.read('gkit.config')
CLIENT_ID = config.get('client', 'clientid')
CLIENT_KEY = config.get('client', 'clientkey')
CLIENT_SECRET = config.get('client', 'clientsecret')
HOST = config.get('grpc', 'host')
PORT = int(config.get('grpc', 'port'))

### COMMON : Client Credentials ###

def set_grpcserver(host='', port=''):
    global HOST
    global PORT

    HOST = host
    PORT = port

def set_clientkey(clientid='', clientkey='', clientsecret=''):
    global CLIENT_ID
    global CLIENT_KEY
    global CLIENT_SECRET

    CLIENT_ID = clientid
    CLIENT_KEY = clientkey
    CLIENT_SECRET = clientsecret

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

# gRPC channel

g_channel = None
g_stub = None

def grpc_conn():
    global g_channel
    global g_stub

    if g_channel is None:
        g_channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), getCredentials())
    if g_stub is None:
        g_stub = gigagenieRPC_pb2_grpc.GigagenieStub(g_channel)

    return g_stub

def grpc_disconn():
    global g_channel
    global g_stub

    g_channel = None
    g_stub = None

# STT

def _generate_request_voice():

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
    
        for content in audio_generator:

            message = gigagenieRPC_pb2.reqVoice()
            message.audioContent = content
            yield message
            
            rms = audioop.rms(content,2)
            #print_rms(rms)

def getVoice2Text():	

    stub = grpc_conn()

    request = _generate_request_voice()
    print ("Listening ...")

    resultText = ''
    for response in stub.getVoice2Text(request):
        if response.resultCd == 200: # partial
            resultText = response.recognizedText
        elif response.resultCd == 201: # final
            resultText = response.recognizedText
            break
        else: # error
            print (response.resultCd)
            break

    return resultText

# DIALOG : queryByText
def queryByText(text, usersession='0000', deviceid='r-pi'):

    stub = grpc_conn()

    message = gigagenieRPC_pb2.reqQueryText()
    message.queryText = text
    message.userSession = usersession
    message.deviceId = deviceid
		
    response = stub.queryByText(message)

    mesg = ''
    if response.resultCd == 200:
        print ("uword: %s" % (response.uword))
        for a in response.action:
            print (a.mesg)
            print (a.actType)
            mesg = a.mesg
        return mesg
    else:
        print ("Fail: %d" % (response.resultCd))
        return None	 

# TTS : getText2VoiceUrl
def getText2VoiceUrl(text):

    stub = grpc_conn()
		
    response = stub.getText2VoiceUrl(gigagenieRPC_pb2.reqText(lang=0, text=text))

    if response.resultCd == 200:
        return response.url
    else:
        print ("Fail")
        return None

def getText2VoiceStream(text, fname):

    stub = grpc_conn()

    message = gigagenieRPC_pb2.reqText()
    message.lang=0
    message.mode=0
    message.text=text
    writeFile=open(fname,'wb')
    for response in stub.getText2VoiceStream(message):
        #if response.HasField("resOptions"):
            #print ("ResVoiceResult: %d" %(response.resOptions.resultCd))
        if response.HasField("audioContent"):
            #print ("Audio Stream")
            writeFile.write(response.audioContent)
    writeFile.close()

def tts_play(text):
    fname = './tmp.wav'
    getText2VoiceStream(text, fname)
    os.system('mplayer %s' % (fname))
    os.remove(fname)
