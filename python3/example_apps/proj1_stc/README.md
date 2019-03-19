# Smart Trash Can 만들기 프로젝트
AI MAKERS KIT을 이용하여 발화로 쓰레기통을 움직이는 프로젝트입니다.

![Title_image](https://github.com/make1everything1hj/code_factory/blob/master/smart_trash_can.png)
## 1. 필요한 재료
* 미니 휴지통 1개
* 마이크로 서보모터 SG90 1개
* PCA9685 서보모터 컨트롤러 1개
* Step-down DC-DC 컨버터 모듈 1개
* 18650 규격 배터리 홀더 (18650 * 2) 1개
* 18650 규격 배터리 1개

## 2. 배선도
![curcuit](https://github.com/make1everything1hj/code_factory/blob/master/circuit_line2.png)


* Smart Trash Can은 18650 배터리를 통해 구동되며, DC 컨버터를 통해 공급받은 전력이 서보모터 컨트롤러를 통해 SG90 서보모터로 공급된다.
* PCA9685 컨트롤러에서 나온 배선 SDA, SCL, VCC, GND은 메이커스 킷 2번(VCC), 3번(SDA), 5번(SCL), 6번(GND)로 연결된다.
* 소스코드 상 서보모터 SG90는 PCA9685 컨트롤러 0번에 연결되어 있다.


## 3. 소스 파일
* PCA9685.py: SG90 서보모터 구동 드라이버 
* smart_trash_can.py: Smart Trash Can 발화 실행 파일

## 4. 실행 방법
pi@raspberrypi:~/ai-makers-kit/ex_app/proj1_stc $ python smart_trash_can.py

## 5. 실행 동영상
[![Alt text for your video](https://img.youtube.com/vi/LSxxszpk2NE/0.jpg)](http://www.youtube.com/watch?v=LSxxszpk2NE)
