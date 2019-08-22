from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from .models import clothes
import datetime
from django.shortcuts import render

def index(request):
    return render(request, 'clothes/index.html', {})





'''
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    clothesData = clothes.objects.all()  # 테이블 데이타를 전부 가져오기 위한 메소드
    context = {'clothesData': clothes}
    try:
        clothesdatas = clothesData(kind=request.POST['kind'], name=request.POST['name'], price=request.POST['price'],
                                 size=request.POST['size'])
        clothesdatas.save()
    except:
        clothesdatas = None
    return render(request, 'clothes/index.html', context)  # render는 view에서 템플릿에 전달할 데이타를 Dictionary로 전달한다


'''
