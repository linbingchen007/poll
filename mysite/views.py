# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext, loader
from django.forms import ModelForm
from django.core.context_processors import csrf
import random
from mysite.forms import LoginForm, RegForm, AdminForm
from mysite.models import User, Admin, Pic, Question, User_Choice_Rel, User_Question, Valid, Choice
from django.db.models import Q
import md5
from datetime import datetime
from django.utils import timezone
DEBUG = False

def init(request):
    #删除数据库所有数据
    Pic.objects.all().delete()
    User.objects.all().delete()
    Valid.objects.all().delete()
    Question.objects.all().delete()
    Admin.objects.all().delete()
    Admin(username = "admin", password = "admin").save()
    return HttpResponse('OK!')


# Create your views here.
@csrf_exempt
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST, request.FILES)
        if form.is_valid():
            tsn = request.FILES['docfile'].name
            uid = request.POST['idsn']
            newdoc = Pic(docfile = request.FILES['docfile'], uid = uid)
            newdoc.save()            
            request.FILES['docfile'].seek(0)
            m1 = md5.new()
            m1.update(request.FILES['docfile'].read())
            if len(User.objects.all().filter(idsn = uid)) >= 1 :
                valids = Valid.objects.all().filter(uid = uid)
                if len(valids) == 0 :
                    Valid(uid = uid, key = m1.hexdigest()).save()
                else:
                    valids[0].key = m1.hexdigest()
                    valids[0].save()
            return HttpResponse(m1.hexdigest() + "/" + uid)
    form = LoginForm()
    documents = Pic.objects.all()
    return render_to_response(
        'mysite/login.html',
        {'form': form, 'documents': documents},
        context_instance=RequestContext(request)
    )

@csrf_exempt
def valid(request, key, uid):
    if uid == None or key == None or key == '' or uid == '':
        return False
    valids = Valid.objects.all().filter(uid = uid)
    if len(valids) >= 1:
        if valids[0].key == key:
            return True
    return False


@csrf_exempt
def reg(request):
    #注册用户
    #对应的网页模版地址为 mysite/templates/mysite/reg.html
    if chkAdminCookies(request) == None:
        return  HttpResponse("无权限查看！")
    if request.method == 'POST':
        username = request.POST['username']
        idsn = request.POST['idsn']
        form = RegForm(request.POST)
        if form.is_valid():
            qry_usrs = User.objects.all().filter(idsn = idsn)
            if len(qry_usrs) != 0:
                return HttpResponse('用户已存在！')
            newusr = User(
                username=request.POST['username'], idsn=request.POST['idsn'])
            newusr.save()
            return HttpResponse(username)
            #return HttpResponseRedirect(reverse('mysite:reg'))
    form = RegForm()
    usrs = User.objects.all()
    c = {
        'form': form,
        'usrs': usrs,
    }
    return render_to_response('mysite/reg.html', c, context_instance=RequestContext(request))

def chkAdminCookies(request):
    #检查cookies是否合法
    username = request.session.get('username', None)
    password = request.session.get('password', None)
    if username and password:
        qry_usrs = Admin.objects.all().filter(
            username=username).filter(password=password)
        if len(qry_usrs) == 1:
            return qry_usrs[0]
        else:
            return None
    else:
        return None

@csrf_exempt
def admin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        form = AdminForm(request.POST)
        if form.is_valid():
            qry_usrs = Admin.objects.all().filter(username = username, password = password)
            if len(qry_usrs) != 0:
                request.session['username'] = username
                request.session['password'] = password
                return HttpResponseRedirect(reverse('mysite:admin'))
            else:
                return HttpResponse('登录失败！')
    if chkAdminCookies(request):
        return manage(request)
    else:
        form = AdminForm()
        c = {
            'form': form,
        }
        return render_to_response('mysite/adminlogin.html', c, context_instance=RequestContext(request))

@csrf_exempt
def manage(request):
    if chkAdminCookies(request):
        c = {
            'topics' : Question.objects.all()
        }
        return render_to_response('mysite/manage.html', c, context_instance=RequestContext(request))


@csrf_exempt
def createpoll(request):
    if request.method == 'POST':
        topic = request.POST['topic']
        i = 0
        st = None
        dt = None
        sdate_str = request.POST['sdate']
        tdate_str = request.POST['tdate']
        sdate_list = sdate_str.split('-')
        tdate_list = tdate_str.split('-')
        shour = int(request.POST['shour'])
        smin = int(request.POST['smin'])
        thour = int(request.POST['thour'])
        tmin = int(request.POST['tmin'])
        try:
            st = datetime(
                year = int( sdate_list[0]), month = int(sdate_list[1]), day = int(sdate_list[2]), hour = shour, minute = smin)
            dt = datetime(
                year = int( tdate_list[0]), month = int(tdate_list[1]), day = int(tdate_list[2]), hour = thour, minute = tmin)
        except:
            return HttpResponse("非法日期")
        if len(Question.objects.all().filter(text = topic)) != 0:
            return HttpResponse("不要创建标题重复的投票")
        question = Question(text = topic, st = st, dt = dt)
        question.save()
        while True:
            key = "opt" + str(i)
            if key in request.POST:
                opt = request.POST[key]
                Choice(question = question, text = opt).save()
                i += 1
            else:
                break
        return HttpResponseRedirect(reverse('mysite:createpoll'))

    return render_to_response('mysite/createpoll.html', context_instance=RequestContext(request))

def canbevoted(topicid, uid):
    if uid == None or uid == '':
        return False
    topics = Question.objects.all().filter(id = topicid)
    now = timezone.now()
    if len(topics) != 0 and \
         len(User_Question.objects.all().filter(user__idsn = uid, question = topics[0])) == 0 and \
             now >= topics[0].st and \
                 now <= topics[0].dt:
        return True
    else:
        return False

@csrf_exempt
def pollResult(request, topicid):
    topic = Question.objects.all().filter(id = topicid)[0]
    choices = topic.choices.all()
    cnt = 0
    for choice in choices:
        cnt += choice.val
    c = {
        "topic" : topic.text,
        "cnt" : cnt,
        "choices" : choices,
    }
    return render_to_response('mysite/pollresult.html', c, context_instance=RequestContext(request))


@csrf_exempt
def poll(request, topicid):
    topics = Question.objects.all().filter(id = topicid)
    if len(topics) > 0 and \
            (DEBUG or \
            (valid(request, request.session.get('key',None), request.session.get('uid',None)) and canbevoted(topicid, request.session.get('uid',None)))):
        c = {
            "topic" : topics[0],
        }
        return render_to_response('mysite/poll.html', c, context_instance=RequestContext(request))
    else:
        return pollResult(request, topics[0].id)

@csrf_exempt
def pollvote(request, topicid, optid):
    if DEBUG or \
            (valid(request, request.session.get('key',None), request.session.get('uid',None)) and canbevoted(topicid, request.session.get('uid',None))):
        topic = Question.objects.all().filter(id = topicid)[0]
        choices = topic.choices.all()
        curChoice = choices.filter(id = optid)[0]
        curChoice.val += 1
        curChoice.save()
        user = User.objects.all().filter(idsn = request.session.get('uid',None))[0]
        User_Question(user = user, question = topic).save()
        User_Choice_Rel(user = user, choice = curChoice).save()
        return pollResult(request, topicid)
    else:
        return HttpResponse("已经投过票或者投票主题不存在！")

@csrf_exempt
def polls(request, type, key = None, uid = None):
    if not chkAdminCookies(request) and not valid(request, key or request.session.get('key', None), uid or request.session.get('uid', None)):
        return HttpResponse('没有权限查看！')
    if key != None and uid != None:
        request.session['key'] = key
        request.session['uid'] = uid
    topics = None
    try:
        itype = int(type)
    except:
        return HttpResponse("type error!")
    timeNow = timezone.now()
    if itype == 0: #all
        topics = Question.objects.all()
    elif itype == 1: #open
        topics = Question.objects.all().filter(st__lte = timeNow).filter(dt__gt = timeNow)
    else:
        topics = Question.objects.all().filter(Q(st__gt = timeNow) | Q(dt__lte = timeNow))
    c = {
        "topics" : topics,
    }
    return render_to_response('mysite/polls.html', c, context_instance=RequestContext(request))