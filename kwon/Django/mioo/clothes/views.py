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
#        crawling()
#        socketOpen()
        socketClient()
        return render(request, 'clothes/crawling.html')


    elif request.method == "POST":
        pass



