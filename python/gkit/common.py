# -*- coding: utf-8 -*-

"""The Python implementation of GiGA Genie AI Makers Kit"""
# author: CheolMin Lee

from __future__ import print_function
from __future__ import absolute_import

# gRPC
import grpc
import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc

import datetime
import hmac
import hashlib

import pyaudio
import audioop
from six.moves import queue
import wave

import ktkws

# Config for GiGA Genie gRPC
CLIENT_ID = 'YOUR_CLIENT_ID'
CLIENT_KEY = 'YOUR_CLIENT_KEY'
CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
HOST = 'gate.gigagenie.ai'
PORT = 4080

KWSID = ['기가지니', '지니야', '친구야', '자기야']
KWSMODELDATA = "../data/kwsmodel.pack"
KWSSOUNDFILE = "../data/sample_sound.wav"
SSLCERTFILE = "../data/ca-bundle.pem"

# Config for Audio
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 512

### COMMON : Client Credentials ###

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
    with open(SSLCERTFILE, 'rb') as f:
        trusted_certs = f.read()
    sslCred = grpc.ssl_channel_credentials(root_certificates=trusted_certs)

    authCred = grpc.metadata_call_credentials(credentials)

    return grpc.composite_channel_credentials(sslCred, authCred)

# MicrophoneStream - original code in https://goo.gl/7Xy3TT
class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)
# [END audio_stream]

def print_rms(rms):
    out = ''
    for _ in range(int(round(rms/30))):
        out = out + '*'
    
    print (out)

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
    while data:
        # writing to the stream is what *actually* plays the sound.
        stream.write(data)
        data = wf.readframes(chunk)

    # cleanup stuff
    stream.close()
    p.terminate()

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

### KWS

g_kwsid = 1     # default: 지니야

def kws_start():
    rc = ktkws.init(KWSMODELDATA)
    rc = ktkws.start()
    ktkws.set_keyword(g_kwsid)
    
    return rc

def kws_stop():
    ktkws.stop()

def kws_reset():
    ktkws.reset()
    
def kws_setkeyword(wakeword):
    global g_kwsid
    g_kwsid = KWSID.index(wakeword)
    ktkws.set_keyword(g_kwsid)

def kws_detect():

    print ('To start, say \"%s\"' % (KWSID[g_kwsid]))

    with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()

        for content in audio_generator:

            rc = ktkws.detect(content)
            rms = audioop.rms(content,2)
            #print('audio rms = %d' % (rms))

            if (rc == 1):
                play_file(KWSSOUNDFILE)
                return 200

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
def queryByText(text):

    stub = grpc_conn()

    message = gigagenieRPC_pb2.reqQueryText()
    message.queryText = text
    message.userSession = "1234"
    message.deviceId = "yourdevice"
		
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
