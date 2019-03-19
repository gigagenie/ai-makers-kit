GiGA Genie AI Makers Kit을 이용하기 위한 Python 소스 코드입니다.

# Prerequisites

Python 2.x, 3.x를 지원하며 아래 Python 라이브러리 추가 설치가 필요합니다.

* gRPC
* PyAudio

GiGA Genie 음성호출어('기가지니', '지니야' 등) 이용을 위해 GiGA Genie에서 제공하는
shared library와 Python extension이 필요합니다.

* [libkwscmdapi.so (Raspberry Pi용)](https://github.com/gigagenie/ai-makers-kit/blob/master/lib/libkwscmdapi.so)
* [ktkws Python extension module](https://github.com/gigagenie/ai-makers-kit/tree/master/python/install)

# Quick Start

AI Makers Kit 이용을 위해서는 [기가지니 개발자 포털](https://gigagenie.ai)에서 개발자 등록 후
client key를 먼저 발급 받아야 합니다.

INSTALL ...

    $ sudo apt-get install libasound-dev
    $ sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
    $ sudo apt-get install python-pip
    $ sudo pip install pyaudio
    $ sudo pip install grpcio grpcio-tools
    $ sudo cp ../lib/libkwscmdapi.so /usr/local/bin/
    $ sudo /sbin/ldconfig -v
    $ sudo python -m easy_install ./install/ktkws-1.0.1-py2.7-linux-armv7l.egg

SET YOUR CLIENT KEY INFORMATION,

    $ vi gkit.config
    
아래 정보를 기가지니 포털에서 발급 받은 클라이언트 키 정보로 업데이트 하세요.
        
    [client]
    clientid: YOUR_CLIENT_ID
    clientkey: YOUR_CLIENT_KEY
    clientsecret: YOUR_CLIENT_SECRET

and RUN !!!

    $ python main_demo.py
    
# Usage

## 기본이 되는 단위 기능별 사용 예제

음성 호출(Keyword Spotting) 이용(ex1 exmaple code 참조)

    import ktkws
    
    ktkws.init(KWSMODELDATA)   # ../data/kwsmodel.pack 이용
    ktkws.start()
    ktkws.set_keyword(KWSID)   # 0: 기가지니, 1: 지니야(default), 2: 친구야, 3: 자기야
    ktkws.detect(AUDIOSTERAM)  # AUDIOSTREAM: PCM 16000Hz, mono, LINEAR16 LE
    # ktkws.detect() return value가 1이면 detect
 
 음성인식/대화/음성합성 API 이용(ex2~6 example code 참조)
 
 * gRPC 서비스 정의 : [../data/gigagenieRPC.proto](https://github.com/gigagenie/ai-makers-kit/blob/master/data/gigagenieRPC.proto)
 * API
    * getVoice2Text         : 음성인식(Speech-to-text)
    * getText2VoiceUrl      : 음성합성(Text-to-speech) wave file url로 전달
    * getText2VoiceStream   : 음성합성(TTS)을 stream data로 전달
    * queryByText           : Text에 대한 대화해석 결과([기가지니 Dialog Kit](https://github.com/gigagenieDmt/DialogKit-deploymentGuide/wiki) 참조)
    * queryByVoice          : STT한 결과에 대한 대화해석 결과([기가지니 Dialog Kit](https://github.com/gigagenieDmt/DialogKit-deploymentGuide/wiki) 참조)
 
## gkit을 이용한 예제

* sample_keyword.py : 음성호출을 이용한 음성인식/음성합성 이용 예제
* sample_button.py : 버튼을 이용한 음성인식/음성합성 이용 예제
* sample_led.py : 다양한 애니메이션 효과를 준 LED 이용 예제
* main_demo.py : 음성호출/버튼을 함계 이용한 음성인식/음성합성 이용 예제(LED 사용 포함)

### sample_keyword.py

    # gkit 모듈 준비
    import gkit
    
    # KWS 모델데이터를 준비
    gkit.kws_start()
    # 음성호출에 사용할 키워드 세팅: 지니야(default), 기가지니, 친구야, 자기야
    gkit.kws_setkeyword('기가지니')
    # kws_detect() 리턴값이 1 이면 음성 호출어가 감지된 것임
    if gkit.kws_detect() == 1:
        print ('detected')

### sample_button.py

    import gkit
    
    # 버튼이 눌러졌을 때 실행되는 callback
    def callback():
        print ("Button was pressed")

    # 버튼 생성 후 callback 등록
    gkit.get_button().on_press(callback)

### sample_led.py

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

### main_demo.py

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

### Enjoy with AI Makers Kit !
