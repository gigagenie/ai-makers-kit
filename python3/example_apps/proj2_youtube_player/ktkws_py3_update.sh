#!/bin/sh
echo "호출어 파이썬3 버전 업데이트 시작합니다."
cd install
sudo easy_install -m ktkws-1.0.1-py3.5-linux-armv7l.egg
sudo cp -r /usr/local/lib/python2.7/dist-packages/ktkws-1.0.1-py3.5-linux-armv7l.egg/ /usr/local/lib/python3.5/dist-packages/
cd /usr/local/lib/python3.5/dist-packages/ktkws-1.0.1-py3.5-linux-armv7l.egg/
sudo cp ktkws.cpython-35m-arm-linux-gnueabihf.so ktkws.py ktkws.pyc ../
sudo rm -r /usr/local/lib/python2.7/dist-packages/ktkws-1.0.1-py3.5-linux-armv7l.egg/
sudo easy_install ~/ai-makers-kit/python/install/ktkws-1.0.1-py2.7-linux-armv7l.egg
