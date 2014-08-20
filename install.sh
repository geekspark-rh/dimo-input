#!/bin/bash

yum install -y opencv opencv-devel numpy opencv-python git
mkdir ./vendor ; cd ./vendor ; git clone https://github.com/opiate/SimpleWebSocketServer.git ; cd ..

