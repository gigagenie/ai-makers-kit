# YouTube Music Video Player 만들기 프로젝트
AI MAKERS KIT을 이용하여 발화로 유튜브 동영상(뮤직 비디오 포함)을 재생하는 프로젝트입니다.

![Title_image](https://github.com/make1everything1hj/code_factory/blob/master/thumbnail.png)
## 1. 필요한 재료
* 모니터 혹은 7인치 LCD Display

## 2. 사전 준비
본 프로젝트는 파이썬3 버전에서 정상 동작합니다.
### 2-1. 환경 구축
#### 2-1-1. 파이썬3 버전 호출어 업데이트

아래 명령어 통해 파이썬3 버전 호출어로 업데이트 합니다.

pi@raspberrypi:~/ai-makers-kit/ex_app/proj2_youtube_mvp $ sudo ./ktkws_py3_update.sh

#### 2-1-2. 관련 라이브러리 설치
아래 명령어를 통해 관련 라이브러리를 설치합니다.

sudo pip3 install pyaudio

sudo pip3 install grpcio grpcio-tools

sudo pip3 install selenium

sudo pip3 install bs4

sudo dpkg -i chromium-chromedriver_65.0.3325.181-0ubuntu0.14.04.1_armhf.deb


## 3. 소스 파일
* ktkws_py3_update.sh: 파이썬3 호출어 버전 업데이트
* proj2_yt_mvp.py: 유튜브 뮤직 비디오 플레이어 재생 프로그램

## 4. 실행 방법
pi@raspberrypi:~/ai-makers-kit/ex_app/proj2_youtube_mvp $ python3 proj2_yt_mvp.py

## 5. 실행 동영상
[![Alt text for your video](https://img.youtube.com/vi/Oh_5-m8I0co/0.jpg)](http://www.youtube.com/watch?v=Oh_5-m8I0co)
