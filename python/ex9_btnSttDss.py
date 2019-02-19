#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Date:2019.02.18
Example 9: 버튼 음성인식 대화 결합 예제
"""

from __future__ import print_function

import grpc

import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc
import os
import datetime
import time
import hmac
import hashlib
import ex1_kwstest as kws
import ex2_getVoice2Text as gv2t
import ex4_getText2VoiceStream as tts
import ex6_queryVoice as dss

'''
본 예제는 1번, 2번, 4번, 6번 예제에 
사용자 인증 정보가 기재되어야 정상 동작합니다.
(CLIENT_ID, CLIENT_KEY, CLIENT_SECRET)
'''

# Config for GiGA Genie gRPC
CLIENT_ID = ''
CLIENT_KEY = ''
CLIENT_SECRET = ''
HOST = 'gate.gigagenie.ai'
PORT = 4080
	
def main():
	#Example8 Button+STT+DSS
	KWSID = ['기가지니', '지니야', '친구야', '자기야']
	while 1:
		recog = kws.btn_test(KWSID[0])
		if recog == 200:
			print('KWS Dectected ...\n Start STT...')
			text = dss.queryByVoice()
			tts_result = tts.getText2VoiceStream(text, "result_mesg.wav")
			if text == '':
				print('질의한 내용이 없습니다.')
			elif tts_result == 500:
				print("TTS 동작 에러입니다.\n")
				break
			else:
				kws.play_file("result_mesg.wav")
			time.sleep(2)
		else:
			print('KWS Not Dectected ...')

if __name__ == '__main__':
    main()