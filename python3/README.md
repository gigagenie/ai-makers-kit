KT AI Coding Pack을 이용하기 위한 Python 3버전 소스 코드입니다.

# 1. Prerequisites
Python 3.x를 지원하며 아래 Python 라이브러리 추가 설치가 필요합니다.

* gRPC
* PyAudio

GiGA Genie 음성호출어('기가지니', '지니야' 등) 이용을 위해 GiGA Genie에서 제공하는
shared library와 Python extension이 필요합니다.

* [libkwscmdapi.so (Raspberry Pi용)](https://github.com/gigagenie/ai-makers-kit/blob/master/lib/libkwscmdapi.so)
* [ktkws Python extension module](https://github.com/gigagenie/ai-makers-kit/tree/master/python/install)

# 2. Quick Start
### a) 사용자 인증정보 받기
&nbsp;&nbsp;AI Makers Kit 이용을 위해서는 [KT APILINK 사이트](https://apilink.kt.co.kr)에서 개발자 등록 후  
&nbsp;&nbsp;인증정보(clientid, client key, clientsecret)를 먼저 발급 받아야 합니다.  
  
### b) Python3 버전 추가 라이브러리 설치  
   &nbsp;&nbsp;&nbsp;$ sudo easy_install3 pip  
   &nbsp;&nbsp;&nbsp;$ sudo easy_install3 install/ktkws-1.0.1-py3.5-linux-armv7l.egg  
   &nbsp;&nbsp;&nbsp;$ sudo apt install portaudio19-dev  
   &nbsp;&nbsp;&nbsp;$ sudo pip3 install grpcio grpcio-tools  
   &nbsp;&nbsp;&nbsp;$ sudo pip3 install pyaudio  
  
### c) 사용자 인증 정보 입력  
&nbsp;&nbsp;&nbsp;[user_auth.py 파일에 인증정보 입력]  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;아래 정보를 기가지니 포털에서 발급 받은 클라이언트 키 정보로 업데이트 하세요.  
   &nbsp;&nbsp;&nbsp;[client]  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;clientid: YOUR_CLIENT_ID  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;clientkey: YOUR_CLIENT_KEY  
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;clientsecret: YOUR_CLIENT_SECRET  
### d) 예제 실행(ex1 ~ ex9)  
&nbsp;&nbsp;&nbsp;$ python3 ex1_kwstest.py  
  
# 3. Usage

### a) 기본이 되는 단위 기능별 사용 예제  
&nbsp;&nbsp;ex1) 음성 호출(Keyword Spotting) 이용(code 참조)

    import ktkws
    
    ktkws.init(KWSMODELDATA)   # ../data/kwsmodel.pack 이용
    ktkws.start()
    ktkws.set_keyword(KWSID)   # 0: 기가지니, 1: 지니야(default), 2: 친구야, 3: 자기야
    ktkws.detect(AUDIOSTERAM)  # AUDIOSTREAM: PCM 16000Hz, mono, LINEAR16 LE
    # ktkws.detect() return value가 1이면 detect
   
&nbsp;&nbsp; ex2-6) 음성인식/대화/음성합성 API 이용(code 참조)
 * gRPC 서비스 정의 : [../data/gigagenieRPC.proto](https://github.com/gigagenie/ai-makers-kit/blob/master/data/gigagenieRPC.proto)
 * API
    * getVoice2Text         : 음성인식(Speech-to-text)
    * getText2VoiceUrl      : 음성합성(Text-to-speech) wave file url로 전달
    * getText2VoiceStream   : 음성합성(TTS)을 stream data로 전달
    * queryByText           : Text에 대한 대화해석 결과([기가지니 Dialog Kit](https://github.com/gigagenieDmt/DialogKit-deploymentGuide/wiki) 참조)
    * queryByVoice          : STT한 결과에 대한 대화해석 결과([기가지니 Dialog Kit](https://github.com/gigagenieDmt/DialogKit-deploymentGuide/wiki) 참조)  
    
 &nbsp;&nbsp;ex7-9) 복합 예제(음성/대화/TTS/Button)  
   
 &nbsp;&nbsp;기타) 기능파일
 * user_auth.py         : 사용자 인증 구현  
 * MicrophoneStream.py  : 마이크 스트림 구현  
 
### b) gkit을 이용한 예제

* sample_keyword.py : 음성호출을 이용한 음성인식/음성합성 이용 예제
* sample_button.py : 버튼을 이용한 음성인식/음성합성 이용 예제
* sample_led.py : 다양한 애니메이션 효과를 준 LED 이용 예제
* main_demo.py : 음성호출/버튼을 함계 이용한 음성인식/음성합성 이용 예제(LED 사용 포함)

#### sample_keyword.py

    # gkit 모듈 준비
    import gkit
    
    # KWS 모델데이터를 준비
    gkit.kws_start()
    # 음성호출에 사용할 키워드 세팅: 지니야(default), 기가지니, 친구야, 자기야
    gkit.kws_setkeyword('기가지니')
    # kws_detect() 리턴값이 1 이면 음성 호출어가 감지된 것임
    if gkit.kws_detect() == 1:
        print ('detected')

#### sample_button.py

    import gkit
    
    # 버튼이 눌러졌을 때 실행되는 callback
    def callback():
        print ("Button was pressed")

    # 버튼 생성 후 callback 등록
    gkit.get_button().on_press(callback)

#### sample_led.py

    import gkit
    
    # LED 객체 생성
    led = gkit.get_led()
    
    # LED로 나타낼 상태 애니메이션 설정
    led.set_state(gkit.LED.BLINK)
    """
    사용 가능한 LED 상태 값
        gkit.LED.OFF
        gkit.LED.ON
        gkit.LED.BLINK
        gkit.LED.BLINK_3
        gkit.LED.BEACON
        gkit.LED.BEACON_DARK
        gkit.LED.DECAY
        gkit.LED.PULSE_SLOW
        gkit.LED.PULSE_QUICK
    """

#### main_demo.py

    import gkit
    
    # 음성호출이나 버튼이 눌러졌을 때 실행되는 callback
    def myservice():
        """ Do something: your service ... """
        # for example : Speech-to-text
        stt_text = gkit.getVoice2Text()
    
    # 클라이언트 키 정보 설정
    gkit.set_clientkey(CLIENT_ID, CLIENT_KEY, CLIENT_SECRET)
    
    # Detector 객체 생성(음성호출, 버튼에 대한 detection 처리)
    detector = gkit.KeywordDetector()
    try:
        detector.start(callback = myservice)
    except:
        detector.terminate()

## Enjoy with KT AI Coding Pack !
