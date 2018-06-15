GiGA Genie AI Makers Kit을 이용하기 위한 Python 소스 코드입니다.

## Prerequisites

Python 2.x, 3.x를 지원하며 아래 Python 라이브러리 추가 설치가 필요합니다.

* gRPC
* PyAudio

GiGA Genie 음성호출어('기가지니', '지니야' 등) 이용을 위해 GiGA Genie에서 제공하는
shared library와 Python extension이 필요합니다.

* [libkwscmdapi.so (Raspberry Pi용)](https://github.com/gigagenie/ai-makers-kit/blob/master/lib/libkwscmdapi.so)
* [ktkws Python extension module](https://github.com/gigagenie/ai-makers-kit/tree/master/python/install)

## Quick Setup

    $ sudo apt-get install libasound-dev
    $ sudo apt-get install libportaudio2
    $ sudo apt-get install python-pip
    $ sudo pip install pyaudio
    $ sudo pip install grpcio grpcio-tools
    $ sudo cp ../lib/libkwscmdapi.so /usr/local/bin/
    $ sudo /sbin/ldconfig -v
    $ sudo python -m easy_install ./install/ktkws-1.0.1-py2.7-linux-armv7l.egg
    
## Usage

AI Makers Kit 이용을 위해서 개발자 등록과 client key를 먼저 발급 받아야 합니다.(링크 제공 예정)

음성 호출(Keyword Spotting) 이용

    import ktkws
    
    ktkws.init(KWSMODELDATA)   # ../data/kwsmodel.pack 이용
    ktkws.start()
    ktkws.set_keyword(KWSID)   # 0: 기가지니, 1: 지니야, 2: 친구야, 3: 자기야
    ktkws.detect(AUDIOSTERAM)  # AUDIOSTREAM: PCM 16000Hz, mono, LINEAR16 LE
    # ktkws.detect() return value가 1로 detect 여부 판단
 
 음성인식/대화/음성합성 API 이용(ex2~6 example code 참조)
 
 * gRPC 서비스 정의 : [../data/gigagenieRPC.proto](https://github.com/gigagenie/ai-makers-kit/blob/master/data/gigagenieRPC.proto)
 * API
    * getVoice2Text         : 음성인식(Speech-to-text)
    * getText2VoiceUrl      : 음성합성(Text-to-speech) wave file url로 전달
    * getText2VoiceStream   : 음성합성(TTS)을 stream data로 전달
    * queryByText           : Text에 대한 대화해석 결과(기가지니 Dialog Kit 참조)
    * queryByVoice          : STT한 결과에 대한 대화해석 결과(기가지니 Dialog Kit 참조)
 
