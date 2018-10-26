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

import pyaudio
import audioop
from six.moves import queue

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 512


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
    with open('/home/pi/ai-makers-kit/data/ca-bundle.pem', 'rb') as f:
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
            print ("ResVoiceResult: %d" %(response.resOptions.resultCd))
        if response.HasField("audioContent"):
            print ("Audio Stream")
            writeFile.write(response.audioContent)
    writeFile.close()

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
    while len(data) > 0:
        # writing to the stream is what *actually* plays the sound.
        stream.write(data)
        data = wf.readframes(chunk)

        # cleanup stuff.
    stream.close()
    p.terminate() 

	
	
def main():
    #getText2VoiceStream("지금부터 열 두개의 명령어로 RC CAR 제어를 시작합니다. 종료를 원하시면 종료라고 말씀해 주세요.","./testtts.wav")
	'''
	getText2VoiceStream("앞으로 이동합니다.","./rc_forward.wav")
	getText2VoiceStream("뒤로 이동합니다.","./rc_backward.wav")
	getText2VoiceStream("바퀴를 우측 방향으로 이동합니다.","./rc_wheel_right.wav")
	getText2VoiceStream("바퀴를 좌측 방향으로 이동합니다.","./rc_wheel_left.wav")
	getText2VoiceStream("바퀴를 정렬합니다.","./rc_wheel_center.wav")
	getText2VoiceStream("카메라를 위로 올립니다.","./rc_cam_up.wav")
	getText2VoiceStream("카메라를 아래로 내립니다.","./rc_cam_down.wav")
	getText2VoiceStream("카메라를 오른쪽 방향으로 이동합니다.","./rc_cam_right.wav")
	getText2VoiceStream("카메라를 왼쪽 방향으로 이동합니다.","./rc_cam_left.wav")
	'''
	getText2VoiceStream("감사합니다.","./stc_thanku.wav")
	play_file("./stc_thanku.wav")
	

if __name__ == '__main__':
    main()
