
#! /usr/bin/python
# -*- coding: utf-8 -*-

from socket import *
from select import *
import sys
from time import ctime


def socketOpen():
    HOST = '172.16.110.171'
#    HOST = '127.0.0.1'
    PORT = 10000
    BUFSIZE = 1024
    ADDR = (HOST, PORT)

    # 소켓 생성
    serverSocket = socket(AF_INET, SOCK_STREAM)

    # 소켓 주소 정보 할당
    serverSocket.bind(ADDR)
    print('bind')

    # 연결 수신 대기 상태
    serverSocket.listen(100)
    print('listen')

    # 연결 수락
    clientSocket, addr_info = serverSocket.accept()
    print('accept')
    print('--clinet information--')
    print(clientSocket)

    # 클라이언트로부터 메시지를 가져옴
    while True:
        data = clientSocket.recv(65535)
        print('recieve data : ', data.decode())
        msg = data.decode()
        if msg == 'exit':
            break

    # 소켓 종료
    clientSocket.close()
    serverSocket.close()
    print('close')

def socketClient():
#    HOST = '127.0.0.1'
    HOST = '172.16.110.171'

    PORT = 10000
    BUFSIZE = 1024
    ADDR = (HOST, PORT)

    clientSocket = socket(AF_INET, SOCK_STREAM)  # 서버에 접속하기 위한 소켓을 생성한다.

    try:
        clientSocket.connect(ADDR)  # 서버에 접속을 시도한다.

    except  Exception as e:
        print('%s:%s' % ADDR)
        sys.exit()

    print('connect is success')

    while True:
        sendData = input("input data : ") + "\n"
        clientSocket.send(sendData.encode())
        print("send success")

def connect(clientSocket, ADDR): # 서버에 소켓 접속
    try:
        clientSocket.connect(ADDR)  # 서버에 접속을 시도한다.

    except  Exception as e:
        print('%s:%s' % ADDR)
        sys.exit()

    print('connect is success')

def sendData(clientSocket, data):
    data = data+'\n'
    print(data)
    clientSocket.send(data.encode())
    print(data.encode())
    return "send success"