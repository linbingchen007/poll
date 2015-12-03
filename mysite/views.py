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
from mysite.forms import LoginForm, RegForm, AdminForm, RegExlForm, LoginpwdForm
from mysite.models import User, Admin, Pic, Question, User_Choice_Rel, User_Choice2_Rel, User_Question, Valid, Choice, \
    Choice2, Candidate, Var, Log, Exl
from django.db.models import Q
import md5,string,xlrd,os,random
from datetime import datetime
from django.utils import timezone
DEBUG = True

def getGloVar(key):
    return Var.objects.all().filter(name = key)[0].val

def setGloVar(key, val):
    obj = Var.objects.all().filter(name = key)[0]
    obj.val = val
    obj.save()

def crypt(key):
    m1 = md5.new()
    m1.update(key[0 : len(key) - 1])
    m1.update(key[1 : len(key)])
    m1.update(key[1 : len(key) - 1])
    m1.update(m1.hexdigest())
    for i in range(len(key) - 1, 0 , -1):
        m1.update(key[i])
    m1.update(Var.objects.all().filter(name = "seed")[0].val)
    return m1.hexdigest()


def init(request):
    #删除数据库所有数据
    if DEBUG :
        Pic.objects.all().delete()
        User.objects.all().delete()
        Valid.objects.all().delete()
        Question.objects.all().delete()
        Admin.objects.all().delete()
        Var.objects.all().delete()
        Candidate.objects.all().delete()
        Exl.objects.all().delete()
        Log.objects.all().delete()
    if DEBUG or Var.objects.all().filter("bind") == None:
        Var(name = "authkey", val = "10000").save()
        Var(name = "bind", val = "0").save()
        Var(name = "seed", val = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))).save()
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

def addVoter(name, idsn, phone):
    chkobjs = User.objects.all().filter(idsn = idsn)
    if len(chkobjs) == 0:
        User(idsn = idsn, username = name, phone = phone).save()

@csrf_exempt
def regexl(request):
    if chkAdminCookies(request) == None:
        return  HttpResponse("无权限查看！")
    if request.method == 'POST':
        form = RegExlForm(request.POST, request.FILES)
        if form.is_valid():
            for obj in Exl.objects.all():
                os.remove(obj.docfile.path)
                obj.delete()
            newexl = Exl(docfile = request.FILES['docfile'])
            newexl.save()
            path = newexl.docfile.path
            workbook = xlrd.open_workbook(path)
            worksheet = workbook.sheet_by_index(0)
            try:
                for i in range(1,worksheet.nrows):
                    addVoter(worksheet.cell_value(i,0), worksheet.cell_value(i,1), worksheet.cell_value(i,2))
                return HttpResponse("导入成功！")
            except:
                return HttpResponse("导入异常！")
    form = RegExlForm()
    return render_to_response('mysite/regexl.html', {"form": form}, context_instance=RequestContext(request))


@csrf_exempt
def valid(request, key, uid, pwd = None):
    if (uid == None or uid == "") :
        return False
    if  ( (key == None or key == "") and (pwd == None or pwd == "")):
        return False
    if pwd != None and pwd != "":
        qryRes = User.objects.all().filter(idsn = uid).filter(pwd = pwd)
        if qryRes != None and len(qryRes) > 0:
            return True
        else:
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
            return HttpResponseRedirect(reverse('mysite:reg'))
    form = RegForm()
    usrs = User.objects.all()
    c = {
        'form': form,
        'usrs': usrs,
    }
    return render_to_response('mysite/reg.html', c, context_instance=RequestContext(request))

def chkAdminCookies(request):
    if DEBUG == True:
        return True
    #检查cookies是否合法
    key = request.session.get('authkey', None)
    value = request.session.get('authvalue', None)
    if key and value and int(key) == int(getGloVar("authkey")) - 1 and crypt(key) == value:
        return True
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
        commitcnt = int(request.POST['commitcnt'])
        try:
            st = datetime(
                year = int( sdate_list[0]), month = int(sdate_list[1]), day = int(sdate_list[2]), hour = shour, minute = smin)
            dt = datetime(
                year = int( tdate_list[0]), month = int(tdate_list[1]), day = int(tdate_list[2]), hour = thour, minute = tmin)
        except:
            return HttpResponse("非法日期")
        if len(Question.objects.all().filter(text = topic)) != 0:
            return HttpResponse("不要创建标题重复的投票")
        question = Question(text = topic, st = st, dt = dt, commitcnt = commitcnt)
        question.save()
        while True:
            key = "opt" + str(i)
            if key in request.POST:
                opt = request.POST[key]
                Choice(question = question, text = opt).save()
                i += 1
            else:
                break
        i = 0
        while True:
            key = "opta" + str(i)
            if key in request.POST:
                opt = request.POST[key]
                Choice2(question = question, text = opt).save()
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

def isTopicClosed(topicId):
    timeNow = timezone.now()
    qryRes = Question.objects.all().filter(Q(st__gt = timeNow) | Q(dt__lte = timeNow)).filter(id = topicId)
    if qryRes == None or len(qryRes) == 0:
        return False
    else:
        return True

@csrf_exempt
def pollresult(request, topicid):
    if chkAdminCookies(request) == None:
        return  HttpResponse("无权限查看！")
    topic = Question.objects.all().filter(id = topicid)[0]
    if DEBUG == False and isTopicClosed(topic.id) == False:
        return HttpResponse("投票尚未结束，不能查看结果")
    choices = topic.choices.all()
    choices2 = topic.choices2.all()
    cnt = 0
    cnt2 = 0
    for choice in choices:
        cnt += choice.val
    for choice in choices2:
        cnt2 += choice.val
    c = {
        "topic" : topic.text,
        "cnt" : cnt,
        "choices" : choices,
        "cnt2" : cnt2,
        "choices2" : choices2,
    }
    return render_to_response('mysite/pollresult.html', c, context_instance=RequestContext(request))


@csrf_exempt
def poll(request, topicid):
    topics = Question.objects.all().filter(id = topicid)
    if len(topics) > 0 and \
            (DEBUG or \
            (valid(request, request.session.get('key', None), request.session.get('uid', None), request.session.get('pwd', None)) and canbevoted(topicid, request.session.get('uid',None)))):
        c = {
            "topic" : topics[0],
        }
        request.session["topicid"] = topics[0].id
        return render_to_response('mysite/poll.html', c, context_instance=RequestContext(request))
    else:
        return HttpResponse("您已经投过票了，或者您无权查看投票结果")

@csrf_exempt
def pollvote(request, topicid = None, optid = None):
    if topicid == None and optid == None and request.method == 'POST' :
        topicid = request.session.get("topicid", None)
        if not (topicid != None  and valid(request, request.session.get('key', None), request.session.get('uid', None), request.session.get('pwd', None)) and canbevoted(topicid, request.session.get('uid',None))):
            return HttpResponse("未知错误")
        topic = Question.objects.all().filter(id = topicid)[0]
        choices = topic.choices.all()
        optid = int(request.POST['vote'])
        user = User.objects.all().filter(idsn = request.session.get('uid', None))[0]
        curChoice = choices.filter(id = optid)[0]
        qryRes = User_Choice_Rel.objects.filter(user = user).filter(choice = curChoice)
        if qryRes == None or len(qryRes) == 0:
            curChoice.val += 1
            curChoice.save()
            User_Choice_Rel(user = user, choice = curChoice).save()
        choices2 = topic.choices2.all()
        for choice in choices2:
            if "checkbox" + str(choice.id) in request.POST:
                qryRes = User_Choice2_Rel.objects.filter(user = user).filter(choice2 = choice)
                if qryRes == None or len(qryRes) == 0:
                    choice.val += 1
                    choice.save()
                    User_Choice2_Rel(user = user, choice2 = choice).save()
        qryRes = User_Question.objects.filter(user = user).filter(question = topic)
        if qryRes == None or len(qryRes) == 0:
            topic.pollcnt += 1
            topic.save()
            User_Question(user = user, question = topic).save()

        return HttpResponse("投票成功")
    else:
        return HttpResponse("已经投过票或者投票主题不存在！")

@csrf_exempt
def polls(request, type = 1, key = None, uid = None):
    if not chkAdminCookies(request) and not valid(request, key or request.session.get('key', None), uid or request.session.get('uid', None), request.session.get('pwd', None)):
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
    c = {}
    if itype == 0: #all
        topics = Question.objects.all()
    elif itype == 1: #open
        topics = Question.objects.all().filter(st__lte = timeNow).filter(dt__gt = timeNow)
    else:
        topics = Question.objects.all().filter(Q(st__gt = timeNow) | Q(dt__lte = timeNow))
        c["closedFg"] = True
    c["topics"] = topics
    return render_to_response('mysite/polls.html', c, context_instance=RequestContext(request))


def getPageContent(page, objs = None):
    if objs == None:
        objs =  User.objects.all()
    paginator=Paginator(objs,500)
    try:
        partcontent=paginator.page(page)
    except PageNotAnInteger:
        partcontent=paginator.page(1)
    except EmptyPage:
        partcontent=paginator.page(paginator.num_pages)
    return partcontent

@csrf_exempt
def voters(request, page = 1):
    c = {'items':getPageContent(page)}
    return render_to_response('mysite/voters.html', c, context_instance=RequestContext(request))

@csrf_exempt
def candidates(request):
    c = {
        "candidates" : Candidate.objects.all()
    }
    return render_to_response('mysite/candidates.html', c, context_instance=RequestContext(request))

@csrf_exempt
def getauthkey(request):
    return HttpResponse(getGloVar("authkey"))

@csrf_exempt
def getseed(request):
    if getGloVar("bind") == "0":
        return HttpResponse(getGloVar("seed"))
    else:
        return HttpResponse("已被绑定！")

@csrf_exempt
def bind(request, seed):
    if getGloVar("bind") == "0":
        if seed == getGloVar("seed"):
            setGloVar("bind", "1")
            return HttpResponse("1")
    return HttpResponse("0")

@csrf_exempt
def auth(request, key = None, value = None):
    if key != None and value != None and key == getGloVar("authkey") and crypt(key) == value:
        request.session["authkey"] = key
        request.session["authvalue"] = value
        setGloVar("authkey", str(int(key) + 1))
        return manage(request)
    else:
        return HttpResponse("验证失败！")

@csrf_exempt
def gopagevoters(request):
    return voters(request,request.POST['pagenum'])

def getVotersObjs(type, key):
    if type == 'idsn':
        return User.objects.all().filter(idsn__contains=key)
    elif type == 'name':
        return User.objects.all().filter(username__contains=key)

@csrf_exempt
def qryvoters(request, page = 1):
    if chkAdminCookies(request) == None:
        return  HttpResponse("无权限查看！")
    objs = None
    if request.method == 'POST':
        if 'qrytype' in request.POST:
            type = request.POST['qrytype']
            key = request.POST.get('qrykey','')
            objs = getVotersObjs(type, key)
            request.session['qryvoterstype'] = type
            request.session['qryvoterskey'] = key
        elif 'pagenum' in request.POST:
            objs = getVotersObjs(request.session['qryvoterstype'], request.session['qryvoterskey'])
    c = {'items':getPageContent(page, objs),
         'idsn': True,
         'phone': True,
         'pwd': True,
         'del': True,
         'selected' : request.session.get('qryvoterstype', '')
         }
    return render_to_response('mysite/qryvoters.html', c, context_instance=RequestContext(request))

@csrf_exempt
def delvoter(request, idsn):
    if chkAdminCookies(request) == None:
        return  HttpResponse("无权限查看！")
    User.objects.all().filter(idsn = idsn)[0].delete()
    return qryvoters(request)

@csrf_exempt

@csrf_exempt
def loginpwd(request):
    if request.method == 'POST':
        form = LoginpwdForm(request.POST)
        if form.is_valid():
            uid = request.POST['idsn']
            pwd = request.POST['pwd']
            if len(User.objects.all().filter(idsn = uid).filter(pwd = pwd)) >= 1 :
                request.session['uid'] = uid
                request.session['pwd'] = pwd
                return polls(request, 1)
    form = LoginpwdForm()
    return render_to_response(
        'mysite/loginpwd.html',
        {'form': form},
        context_instance=RequestContext(request)
    )

