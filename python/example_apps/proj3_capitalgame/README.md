# 나라 수도 맞추기 게임 프로젝트
AI MAKERS KIT을 이용하여 발화로 국가의 수도를 맞추는 퀴즈 게임 제작 프로젝트입니다.

## 1. 파이썬 버전
* 지원 버전: Python3

## 2. 사전 준비
본 프로젝트는 파이썬3 버전에서 정상 동작합니다.
### 2-1. 환경 구축
아래 명령어를 통해 관련 라이브러리를 설치합니다.

sudo pip3 install pyaudio

sudo pip3 install grpcio grpcio-tools

## 3. 소스 파일
* captial_game.py: 나라수도 맞추기 게임 코드
* country_capital.txt: 나라와 수도 정보가 저장된 텍스트 파일
* ex2_getVoice2Text.py: 음성인식(STT) 함수 호출을 위한 파일
* ex4_getText2VoiceStream.py: TTS 함수 호출을 위한 파일


## 4. 실행 방법
pi@raspberrypi:~/ai-makers-kit/ex_app/proj3_capital $ python3 proj3_capital_game.py

