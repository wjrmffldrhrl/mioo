from django.shortcuts import render

# Create your views here.
import os
from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.parse import quote
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from operator import eq
from django.http import HttpResponse
from django.http import JsonResponse
from .models import clothes
import datetime
from django.shortcuts import render
from .models import clothes
from django.views.decorators.csrf import csrf_exempt


def getBs(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bs = BeautifulSoup(html, 'html.parser')
    except AttributeError as e:
        return None
    return bs


## 크롤링 해야될 목록들
mainUrl = 'http://modernsweet.co.kr'


def get_category(url):
    bs = getBs(url)
    category = bs.ul.findAll('li', {'class': 'xans-record-'})

    print('category list ')
    count = 1
    for item in category:
        print(count, ')', item.a.get_text())
        count += 1

    while True:
        print('choice category (exit : q)')
        choice = input()
        for item in category:
            if eq(item.a.get_text(), choice):
                return item.a.attrs['href']
            if choice is 'q':
                return None
        print("can't find ", choice)


## 다음 페이지 알아내기

def get_nextpage(url):
    bs = getBs(url)
    next_page = bs.find('img', {'alt': '다음 페이지'})
    next_page = next_page.parent.attrs['href']

    if eq(next_page, '#none'):
        return next_page

    andp = next_page.find('&')  # 구분자 찾기
    next_page = next_page[andp:]
    return next_page

## 페이지 내부에서 옷 목록 가져오기

def get_item(url):
    bs = getBs(url)
    item_list = bs.findAll('div',{'class':'box'})
    count = 1
    for item in item_list:
        try:
            print(count,') name : ',item.img.attrs['alt'])
            print('url :',item.a.attrs['href'])
            count+=1
        except AttributeError as e:
            print('no item')
    return item_list

### 현제 페이지에서 이미지 모두 가져오기
downloadDirectory = 'download'

def getDownloadLink(source):
    mainUrl = 'http://modernsweet.co.kr'
    source = quote(source,safe=':/')
    return mainUrl+source

def get_img(url,filename):
    bs = getBs(url)
    downpath = 'downdown/'+filename+'/'
    item_information = bs.find('div',{'id':'prdDetail'})
    img_list = item_information.findAll('img')
    count = 1
    for img in img_list:
        print(getDownloadLink(img.attrs['ec-data-src']))
        urlretrieve(getDownloadLink(img.attrs['ec-data-src']),downpath+str(count)+'.jpg')
        count+=1

def get_information(url):
    bs = getBs(url)
    info_list = bs.find('div',{'class':'cont'})
    info_list = info_list.findAll('span')
    count = 1
    text = ''
    for info in info_list:
        #print(count,':',info.get_text())
        #count+=1
        text += info.get_text()+'\n'
    return text


def get_infofile(text, filename):
    path = 'downdown/' + filename + '/'
    f = open(path + filename + '.txt', 'w', -1, "utf-8")

    f.write(text)
    f.close()


def crawling():
    global mainUrl
    ## 메뉴 가져오기
    category = get_category(mainUrl)
    if category is None:
        return None
    ##메뉴 크롤링 시작
    print('start crawling')
    target = mainUrl + category
    count = 1
    while 1:
        print(count, ' page')
        ##타겟 페이지 내부의 상품 추출
        item_list = get_item(target)
        for item in item_list:
            try:
                itemName = item.img.attrs['alt']
                itemUrl = item.a.attrs['href']
            except AttributeError as e:
                print('no item')
                break

            os.makedirs('downdown/' + itemName)
            get_img(mainUrl + itemUrl, itemName)
            text = get_information(mainUrl + itemUrl)
            get_infofile(text, itemName)

        if eq(get_nextpage(target), '#none'):
            break
        else:
            target = target + get_nextpage(target)
        count += 1


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
def crawling(request):
    if request.method == "GET":
        res_data = get_category(mainUrl)
        crawling()
        return render(request, 'clothes/crawling.html', res_data)


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


