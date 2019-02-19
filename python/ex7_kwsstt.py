#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Date:2019.02.18
Example 7: 호출어 음성인식 결합 예제
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
import ex2_getVoice2Text as gv2t
import ex1_kwstest as kws

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
	#Example7 KWS+STT

	KWSID = ['기가지니', '지니야', '친구야', '자기야']
	while 1:
		recog=kws.test(KWSID[0])
		if recog == 200:
			print('KWS Dectected ...\n Start STT...')
			text = gv2t.getVoice2Text()
			print('Recognized Text: '+ text)
			time.sleep(2)
			
		else:
			print('KWS Not Dectected ...')

if __name__ == '__main__':
    main()