from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index_view(request):
    return render(request, 'index/index.html', locals())


def test_view(request):
    print('test_view被调用')
    return HttpResponse('请求到达了test_view页面')


import os
from django.conf import settings


def upload_view(request):
    if request.method == 'GET':
        return render(request, 'index/upload.html')
    elif request.method == 'POST':
        a_file = request.FILES['myfile']
        print('上传的文件名：', a_file.name)
        # a_file.file.read() 读取文件
        # 计算文件保存的位置
        filename = os.path.join(settings.MEDIA_ROOT, a_file.name)
        # 保存文件
        try:
            with open(filename, 'wb') as fw:
                fw.write(a_file.file.read())
            return HttpResponse("收到文件"+a_file.name)
        except Exception as err:
            print(err)
            return HttpResponse('文件上传失败')
