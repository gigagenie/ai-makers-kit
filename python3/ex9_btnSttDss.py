#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Date:2019.02.18
Example 9: 버튼 음성인식 대화 결합 예제
"""

from __future__ import print_function
import ex1_kwstest as kws
import ex4_getText2VoiceStream as tts
import ex6_queryVoice as dss
import MicrophoneStream as MS
import time
	
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
				MS.play_file("result_mesg.wav")
			time.sleep(2)
		else:
			print('KWS Not Dectected ...')

if __name__ == '__main__':
    main()