AI Makers Kit을 이용하기 위해 필요한 드라이버 설치 가이드입니다.

1. 라즈비안 설치 후, 패키지를 적절한 폴더에 풀어줍니다. (ex, /home/pi/install)

    $ gzip -cd AIMakersKit-DriverPackage.tgz | tar xf -
    
2. 설치 전에 네트워크가 정상적인 지 확인합니다.
3. 패키지 내부에 쉘 스크립트에 실행 퍼미션이 없으면 추가합니다.

    $ chmod a+x aimk-install.sh after-install.sh
 
4. “aimk-install.sh”파일을 아래와 같이 실행합니다.

    $ ./aimk-install.sh
 
5. 인스톨이 완료까지 기다리면 재부팅 합니다..
6. 재부팅이 되면 “after-install.sh" 파일을 아래와 같이 실행합니다

    $ ./after-install.sh
 
7. 실행 완료 후 재부팅이 되면 정상적으로 음성이 출력되는지 확인합니다.

    $ sh /home/pi/.genie-kit/bin/CheckAudio.sh
