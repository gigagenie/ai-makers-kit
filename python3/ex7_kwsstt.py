#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Date:2019.02.18
Example 7: 호출어 음성인식 결합 예제
"""
from __future__ import print_function

import time
import ex2_getVoice2Text as gv2t
import ex1_kwstest as kws

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