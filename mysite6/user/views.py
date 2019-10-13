from django.shortcuts import render
from . import models
from django.http import HttpResponse, HttpResponseRedirect, Http404
# Create your views here.


def reg_view(request):
    if request.method == 'GET':
        return render(request, 'user/register.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password1 = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        # 验证数据的合法性
        if len(username) < 6:
            username_error = '*用户名太短'
            return render(request, 'user/register.html', locals())
        elif password1 is '':
            password_error = '*密码不能为空'
            return render(request, 'user/register.html', locals())
        elif password1 != password2:
            password2_error = '*两次密码不一致'
            return render(request, 'user/register.html', locals())
        try:
            # 从数据库查找用户，如果查不到则会报错
            auser = models.User.objects.get(username=username)
            username_error = '*用户名已存在'
            return render(request, 'user/register.html', locals())
        except Exception as err:
            user = models.User.objects.create(username=username,
                                              password=password2)
            html = """
                    注册成功！
                    <a href='/user/login'>进入登录界面</a>
                   """
            resp = HttpResponse(html)
            # 添加cookies
            resp.set_cookie('username', username)
            return resp


def login_view(request):
    if request.method == 'GET':
        # 设置session的值
        # request.session['abc'] = 123
        # val = request.session.get('abc', 'xxx')
        # print(val)
        # return HttpResponse('添加成功')
        username = request.COOKIES.get('username')
        if username is None:
            del username
        return render(request, 'user/login.html',locals())
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        if username is '':
            username_error = '*用户名不能为空'
            return render(request, 'user/login.html', locals())
        elif password is '':
            password_error = '*密码不能为空'
            return render(request, 'user/login.html', locals())
        try:
            auser = models.User.objects.get(username=username)
            if auser.password == password:
                # 记录一个登录状态
                request.session['user'] = {
                    'username': username,
                    'id': auser.id  # 记录当前用户的id
                }
                resp = HttpResponseRedirect('/')
                if 'rember' in request.POST:
                    resp.set_cookie('username', username)
                # return HttpResponse('登录成功！')
                return resp
            else:
                password_error = '*密码错误'
                return render(request, 'user/login.html', locals())
        except Exception as err:
            username_error = '*用户不存在'
            return render(request, 'user/login.html', locals())


def logout_view(request):
    "退出登录"
    if 'user' in request.session:
        del request.session['user']  # 清除登录状态
    return HttpResponseRedirect('/')  # 返回主页

from . import forms

def reg2_view(request):
    if request.method == 'GET':
        myform1 = forms.MyregFrom()
        # html = myform1.as_p()
        # print(html)
        return render(request, 'user/reg2.html', locals())
    elif request.method == "POST":
        # form表单取值方法
        myform = forms.MyregFrom(request.POST)
        if myform.is_valid():  # 是可用的
            dic = myform.cleaned_data # 以字典形式获取有效表单值
            # return HttpResponse(str(dic))
            username = dic['username']
            password = dic['password']
            password1 = dic['password2']
            # 进行注册，略
            return HttpResponse(str(dic))
        else:

            return HttpResponse('验证失败')


def mod_passwd_view(request):
    if request.method == 'GET':
        return render(request, 'user/mod_passwd.html')
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        if username is '':
            username_error = '*用户名不能为空'
            return render(request, 'user/mod_passwd.html', locals())
        elif password is '':
            password_error = '*密码不能为空'
            return render(request, 'user/mod_passwd.html', locals())
        elif password2 is '':
            password2_error = '*密码不能为空'
            return render(request, 'user/mod_passwd.html', locals())
        try:
            auser = models.User.objects.get(username=username,
                                            password=password)
            auser.password = password2
            if 'user' in request.session:
                del request.session['user']  # 清除登录状态
            return HttpResponseRedirect('/')  # 返回主页
        except Exception as err:
            username_error = '*用户不存在或密码错误'
            return render(request, 'user/mod_passwd.html', locals())


def failed_view(request):
    print('无效页面')
    return render(request, 'user/404.html')