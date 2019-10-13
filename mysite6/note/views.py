# file : note/views.py
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
from user.models import User
from . import models


def check_login(fn):
    def wrap(request, *args, **kwargs):
        if not hasattr(request, 'session'):  # 没有登录
            return HttpResponseRedirect('/user/login')
        if 'user' not in request.session:  # 没有登录
            return HttpResponseRedirect('/user/login')
        return fn(request, *args, **kwargs)
    return wrap


@check_login
def list_view(request):
    # 此时已登录
    user_id = request.session['user']['id']
    # 根据已登录的用户id 找到当前登录用户
    auser = User.objects.get(id=user_id)
    notes = auser.note_set.all()
    return render(request, 'note/showall.html', locals())


@check_login
def add_view(request):
    if request.method == 'GET':
        return render(request, 'note/add_note.html', locals())
    elif request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        user_id = request.session['user']['id']
        auser = User.objects.get(id=user_id)
        anote = models.Note(user=auser)
        anote.title = title
        anote.content = content
        anote.save()
        return HttpResponseRedirect('/note/')


@check_login
def mod_view(request, note_id):
    # 得到当前登录的用户的模型对象
    user_id = request.session['user']['id']
    auser = User.objects.get(id=user_id)
    anote = models.Note.objects.get(user=auser, id=note_id)
    if request.method == 'GET':
        return render(request, 'note/modify_note.html', locals())
    elif request.method == 'POST':
        anote.title = request.POST.get('title', '')
        anote.content = request.POST.get('content', '')
        anote.save()
        return HttpResponseRedirect('/note/')


@check_login
def del_view(request, note_id):
    # 得到当前登录的用户的模型对象
    user_id = request.session['user']['id']
    auser = User.objects.get(id=user_id)
    anote = models.Note.objects.get(user=auser, id=note_id)
    anote.delete()
    return HttpResponseRedirect('/note/')


from django.core.paginator import Paginator # 导入分页类


@check_login
def list2_view(request):
    # 此时已登录
    user_id = request.session['user']['id']
    # 根据已登录的用户id 找到当前登录用户
    auser = User.objects.get(id=user_id)
    notes = auser.note_set.all()
    # 在此处添加分页功能
    paginator = Paginator(notes, 5)
    # 得到当前页码数
    cur_page = request.GET.get('page', 1)
    cur_page = int(cur_page)
    page = paginator.page(cur_page) # 得到当前页面的内容
    return render(request, 'note/listpage.html', locals())