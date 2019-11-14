from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.http import JsonResponse
from .models import clothes
import datetime
from django.shortcuts import render
from .models import clothes
from django.views.decorators.csrf import csrf_exempt
from .crawling import crawling
from .socket import *
import time

@csrf_exempt
def index(request):
    if request.method == "GET":
        pass
    elif request.method == "POST":

        size = request.POST.get('size', None)
        name = request.POST.get('name', None)
        kind = request.POST.get('kind', None)
        price = request.POST.get('price', None)

        res_data = {} # 응답 메세지를 담을 변수(딕셔너리)


        input_clothes = clothes(
            kind=kind,
            name=name,
            price=price,
            size=size
        )

        input_clothes.save()

        res_data['success'] = True

        return JsonResponse(res_data)

@csrf_exempt
def clothesData(request):
    if request.method == "GET":
        crawling()
#        socketOpen()
#        socketClient()
        return render(request, 'clothes/crawling.html')


    elif request.method == "POST":
        pass


@csrf_exempt
def RemoteControl(request):
    #HOST = '172.16.110.171' # C# 소켓 서버 호스트 주소
    HOST = '127.0.0.1'  # 로컬 테스트 소켓 서버 호스트 주소
    PORT = 10000
    BUFSIZE = 1024
    ADDR = (HOST, PORT)
    clientSocket = socket(AF_INET, SOCK_STREAM)  # 서버에 접속하기 위한 소켓을 생성한다.

    if request.method == "GET":
        #connect(clientSocket, ADDR) # 소켓 서버와 연결
        #socketClient()
        connect(clientSocket, ADDR)  # 소켓 서버와 연결
        sendData(clientSocket, "test data!!!!!")

        res_data = {}
        res_data['success'] = True
        return JsonResponse(res_data)

#        return render(request, 'clothes/RemoteControl.html')


    elif request.method == "POST":
        next = request.POST.get('next', None)
        previous = request.POST.get('previous', None)

        data = "gdgd"
        clientSocket.send(data.encode())

        res_data = {}
        print(next, previous)

        if int(next) == 1:
            sendData(clientSocket, "next")
        if int(previous) == 1:
            sendData(clientSocket, "previous")
        #time.sleep(1) # 소켓 연결 종료 시 이상한거보내짐
        # for문에 time.sleep넣으면 왜 두번돌아

        res_data['success'] = True
        return JsonResponse(res_data)


