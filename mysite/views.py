# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import  render_to_response
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext
from mysite.forms import LoginForm, RegForm, RegExlForm, LoginpwdForm, RegCanditeForm, SetTextForm, RegByJudgeForm
from mysite.models import User, Pic, Question, User_Choice_Rel, User_Choice2_Rel, User_Question, Valid, Choice, \
    Choice2, Candidate, Var, Log, Exl, Text, Judge_Queue
from django.db.models import Q
import md5,string,xlrd,os,random
import re
from datetime import datetime
from django.utils import timezone
DEBUG = False
import logging
logging.basicConfig(format='%(asctime)s %(message)s', filename='operator.log', level=logging.INFO)

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
        Var.objects.all().delete()
        Candidate.objects.all().delete()
        Exl.objects.all().delete()
        Log.objects.all().delete()
        Text.objects.all().delete()
    if DEBUG or Var.objects.all().filter("bind") == None:
        Var(name = "authkey", val = "10000").save()
        Var(name = "bind", val = "0").save()
        Var(name = "seed", val = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(10))).save()
        Text(id = 0, content = "").save()
        Text(id = 1, content = "").save()
        Text(id = 2, content = "").save()
    return HttpResponse('OK!')

@csrf_exempt
def msg(request, backurl, msginf):
    c = {
        "backurl": backurl,
        "msginf": msginf,
    }
    return render_to_response('mysite/msg.html', c, context_instance=RequestContext(request))


# 加密性 和 安全性 有待增强
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

def addVoter(name, idsn, phone, type = 0):
    chkobjs = User.objects.all().filter(idsn = idsn)
    if len(chkobjs) == 0:
        User(idsn = idsn, username = name, phone = phone, type = int(type)).save()
    else:
        chkobjs[0].username = name
        chkobjs[0].phone = phone
        try:
            chkobjs[0].type = int(type)
        except:
            chkobjs[0].type = 0
        chkobjs[0].save()


@csrf_exempt
def regexl(request):
    if chkAdminCookies(request) == None:
        return msg(request, "mysite:index", "无权限查看！")
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
                    if worksheet.ncols == 3:
                        addVoter(worksheet.cell_value(i,0), worksheet.cell_value(i,1), worksheet.cell_value(i,2))
                    elif worksheet.ncols == 4:
                        addVoter(worksheet.cell_value(i,0), worksheet.cell_value(i,1), worksheet.cell_value(i,2), worksheet.cell_value(i,3))
                    else:
                        raise
                return msg(request, "mysite:regexl", "导入成功！")
            except:
                return msg(request, "mysite:regexl", "导入异常！")
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
        return msg(request, "mysite:index", "无权限查看！")
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            username = request.POST['username'].strip()
            idsn = request.POST['idsn'].strip()
            phone = request.POST['phone'].strip()
            type = int(request.POST['type'])
            qry_usrs = User.objects.all().filter(idsn = idsn)
            if len(qry_usrs) != 0:
                qry_usrs[0].username = username
                qry_usrs[0].phone = phone
                qry_usrs[0].save()
                msg(request, "mysite:reg", '用户已存在并重新修改！')
            newusr = User(username = username, idsn = idsn, phone = phone, type = type, suffix = idsn[14:18])
            newusr.save()
            return msg(request, "mysite:reg", "注册成功！")
        return msg(request, "mysite:reg", "关键项未填!")
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
    timeNow = timezone.now()
    pollsRunning = Question.objects.all().filter(st__lte = timeNow).filter(dt__gt = timeNow)
    if pollsRunning != None and len(pollsRunning) > 0:
        return None
    if key and value and int(key) == int(getGloVar("authkey")) - 1 and crypt(key) == value:
        return True
    else:
        return None

@csrf_exempt
def admin(request):
    if chkAdminCookies(request):
        logging.info("管理员 进入 管理页面")
        return manage(request)
    return render_to_response('mysite/adminlogin.html', context_instance=RequestContext(request))

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
            return msg(request, "mysite:createpoll", "非法日期")
        if len(Question.objects.all().filter(text = topic)) != 0:
            return msg(request, "mysite:createpoll", "不要创建标题重复的投票")
        question = Question(text = topic, st = st, dt = dt, commitcnt = commitcnt)
        question.save()
        while True:
            key = "opt" + str(i)
            if key in request.POST:
                opt = request.POST[key]
                optStrs = re.compile('[\s|　]+').split(opt)
                qryObjs = User.objects.all().filter(username = optStrs[0]).filter(suffix = optStrs[1])
                if qryObjs != None and len(qryObjs) > 0:
                    Choice(question = question,  text = qryObjs[0], type = 0).save()
                else:
                    question.delete()
                    return msg(request, "mysite:createpoll", "添加失败！存在未登记的候选人！")
                i += 1
            else:
                break
        i = 0
        while True:
            key = "opta" + str(i)
            if key in request.POST:
                opt = request.POST[key]
                optStrs = re.compile('[\s|　]+').split(opt)
                qryObjs = User.objects.all().filter(username = optStrs[0]).filter(suffix = optStrs[1])
                if qryObjs != None and len(qryObjs) > 0:
                    Choice2(question = question, text = qryObjs[0], type = 0).save()
                else:
                    question.delete()
                    return msg(request, "mysite:createpoll", "添加失败！存在未登记的候选人！")
                i += 1
            else:
                break
        return msg(request, "mysite:createpoll", "添加投票成功！")
    czObjs = Candidate.objects.all().filter(eletype = 1)
    wyObjs = Candidate.objects.all().filter(eletype = 0)
    c = {
        "cnt1": len(czObjs),
        "cnt0": len(wyObjs),
        "czs": czObjs,
        "wys": wyObjs,
    }
    return render_to_response('mysite/createpoll.html', c, context_instance=RequestContext(request))

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
def pollresult(request, topicid, type = 0):
    if chkAdminCookies(request) == None:
        return  msg(request, "mysite:index", "无权限查看！")
    topic = Question.objects.all().filter(id = topicid)[0]
    if DEBUG == False and isTopicClosed(topic.id) == False:
        return msg(request, "mysite:index", "投票尚未结束，不能查看结果")
    if int(type) == 0:
        c = {
            "topic" : topic,
            "type": 0,
        }
    elif int(type) == 1:
        choices = topic.choices.all().order_by('-val')
        cnt = 0
        for choice in choices:
            cnt += choice.val
        c = {
            "topic" : topic,
            "cnt" : cnt,
            "choices" : choices,
            "type": 1,
        }
    else:
        choices2 = topic.choices2.all().order_by('-val')
        cnt2 = 0
        for choice in choices2:
            cnt2 += choice.val
        c = {
            "topic" : topic,
            "cnt2" : cnt2,
            "choices2" : choices2,
            "type": 3,
        }
    return render_to_response('mysite/pollresult.html', c, context_instance=RequestContext(request))


@csrf_exempt
def poll(request, topicid):
    topics = Question.objects.all().filter(id = topicid)
    if len(topics) > 0 and \
            ( \
            (valid(request, request.session.get('key', None), request.session.get('uid', None), request.session.get('pwd', None)) and canbevoted(topicid, request.session.get('uid',None)))):
        wyObjs = Choice2.objects.all().filter(question = topics[0]).filter(type = 0)
        c = {
            "topic" : topics[0],
            "choices": Choice.objects.all().filter(question = topics[0]).filter(type = 0),
            "choices2": wyObjs,
            "cnt0": len(wyObjs),
        }
        request.session["topicid"] = topics[0].id
        return render_to_response('mysite/poll.html', c, context_instance=RequestContext(request))
    else:
        return pollresult(request, topicid)

def getUser(Str):
    nameSuffix = re.compile('[\s|　]+').split(Str)
    if len(nameSuffix) == 1:
        userObjs = User.objects.all().filter(username= nameSuffix[0])
        if len(userObjs) == 1:
            return userObjs[0]
        else:
            return None
    elif len(nameSuffix) == 2:
        userObjs = User.objects.all().filter(username= nameSuffix[0]).filter(suffix = nameSuffix[1])
        if len(userObjs) == 1:
            return userObjs[0]
        else :
            return None
    else:
        return None

def getChoice(question, text):
    qryObjs = Choice.objects.all().filter(question = question).filter(text = text)
    if len(qryObjs) == 1:
        return qryObjs[0]
    elif len(qryObjs) == 0:
        newChoice = Choice(question = question, text = text)
        newChoice.save()
        return newChoice
    else:
        return None

def getChoice2(question, text):
    qryObjs = Choice2.objects.all().filter(question = question).filter(text = text)
    if len(qryObjs) == 1:
        return qryObjs[0]
    elif len(qryObjs) == 0:
        newChoice = Choice2(question = question, text = text)
        newChoice.save()
        return newChoice
    else:
        return None

@csrf_exempt
def pollvote(request, topicid = None, optid = None):
    if topicid == None and optid == None and request.method == 'POST' :
        topicid = request.session.get("topicid", None)
        if not (topicid != None  and valid(request, request.session.get('key', None), request.session.get('uid', None), request.session.get('pwd', None)) and canbevoted(topicid, request.session.get('uid',None))):
            return msg(request, "mysite:index", "未知错误")
        topic = Question.objects.all().filter(id = topicid)[0]
        cz = getUser(request.POST['vote'])
        ######!!!!!!!!!!!
        user = User.objects.all().filter(idsn = request.session.get('uid', None))[0]
        curChoice = getChoice(topic, cz)
        qryRes = User_Choice_Rel.objects.filter(user = user).filter(choice = curChoice)
        if qryRes == None or len(qryRes) == 0:
            curChoice.val += 1
            curChoice.save()
            User_Choice_Rel(user = user, choice = curChoice).save()
        wyCnt = int(request.POST['wycnt'])
        checkedCnt = 0
        for i in range(wyCnt):
            if "checkbox" + str(i) in request.POST:
                checkedCnt += 1
            if checkedCnt > topic.commitcnt:
                return msg(request, "mysite:index", "选举的委员数量多于限定值！")
        for i in range(wyCnt):
            if "checkbox" + str(i) in request.POST:
                curChoice = getChoice2(topic, getUser(request.POST["checkbox" + str(i)]))
                qryRes = User_Choice2_Rel.objects.filter(user = user).filter(choice2 = curChoice)
                if qryRes == None or len(qryRes) == 0:
                    curChoice.val += 1
                    curChoice.save()
                    User_Choice2_Rel(user = user, choice2 = curChoice).save()
        qryRes = User_Question.objects.filter(user = user).filter(question = topic)
        if qryRes == None or len(qryRes) == 0:
            topic.pollcnt += 1
            topic.save()
            User_Question(user = user, question = topic).save()

        return msg(request, "mysite:index", "投票成功")
    else:
        return msg(request, "mysite:index", "已经投过票或者投票主题不存在！")

@csrf_exempt
def polls(request, type = 1, key = None, uid = None):
    if not chkAdminCookies(request) and not valid(request, key or request.session.get('key', None), uid or request.session.get('uid', None), request.session.get('pwd', None)):
        return msg(request, "mysite:index", '没有权限查看！')
    if key != None and uid != None:
        request.session['key'] = key
        request.session['uid'] = uid
    topics = None
    try:
        itype = int(type)
    except:
        return msg(request, "mysite:index", "类型错误!")
    timeNow = timezone.now()
    c = {}
    if itype == 0: #all
        topics = Question.objects.all()
        c["listtype"] = 0
    elif itype == 1: #open
        topics = Question.objects.all().filter(st__lte = timeNow).filter(dt__gt = timeNow)
        c["listtype"] = 1
    else:
        topics = Question.objects.all().filter(Q(st__gt = timeNow) | Q(dt__lte = timeNow))
        c["listtype"] = 2
    c["topics"] = topics
    return render_to_response('mysite/polls.html', c, context_instance=RequestContext(request))


def getPageContent(page, objs = None, type = 0):
    if objs == None:
        if type == 0:
            objs =  User.objects.all()
        elif type == 1:
            objs =  Candidate.objects.all()
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
    if request.method == 'POST':
        page = request.POST['pagenum']
    c = {'items': getPageContent(page),
         'username': True,
         'listurl': 'mysite:voters',
         }
    return render_to_response('mysite/voters.html', c, context_instance=RequestContext(request))

@csrf_exempt
def candidates(request):
    c = {
        "candidates0" : Candidate.objects.all().filter(eletype = 0),
        "candidates1" : Candidate.objects.all().filter(eletype = 1),
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
        return User.objects.all().filter(idsn__contains = key)
    elif type == 'name':
        return User.objects.all().filter(username__contains = key)

def getCandidatesObjs(type, key):
    if type == 'name':
        return Candidate.objects.all().filter(user__username__contains = key)


@csrf_exempt
def qryvoters(request, page = 1):
    if chkAdminCookies(request) == None:
        return  msg(request, "mysite:index", "无权限查看！")
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
            page = request.POST['pagenum']
    c = {'items':getPageContent(page, objs),
         'listurl': 'mysite:qryvoters',
         'delurl': 'mysite:delvoter',
         'username': True,
         'idsn': True,
         'phone': True,
         'pwd': True,
         'del': True,
         'type': True,
         'selected' : request.session.get('qryvoterstype', '')
         }
    return render_to_response('mysite/qryvoters.html', c, context_instance=RequestContext(request))

@csrf_exempt
def delvoter(request, id):
    if chkAdminCookies(request) == None:
        return  msg(request, "mysite:index", "无权限查看！")
    User.objects.all().filter(id = id)[0].delete()
    return qryvoters(request)


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
                request.session.set_expiry(3600*3)
                return polls(request, 1)
    c = {}
    if valid(request, request.session.get('key', None), request.session.get('uid', None), request.session.get('pwd', None)):
        c['uid'] = request.session.get('uid', None)
    form = LoginpwdForm()
    c['form'] = form
    return render_to_response('mysite/loginpwd.html', c, context_instance=RequestContext(request))

@csrf_exempt
def clearlogincookies(request):
    del request.session['uid']
    del request.session['pwd']
    request.session.modified = True
    return HttpResponseRedirect(reverse('mysite:loginpwd'))


@csrf_exempt
def addcandidate(request):
    if chkAdminCookies(request) == None:
        return  msg(request, "mysite:index", "无权限查看！")
    if request.method == 'POST':
        form = RegCanditeForm(request.POST, request.FILES)
        if form.is_valid():
            if request.POST['picfile'] == '':
                picfile = None
            else:
                picfile = request.FILES['picfile']
            eletype = request.POST['eletype']
            sex = request.POST['sex']
            birthyear = request.POST['birthyear'].strip()
            backgroud = request.POST['backgroud']
            nation = request.POST['nation']
            videourl = request.POST['videourl'].strip()
            politics = request.POST['politics']
            othertext = request.POST['othertext']
            idsn = request.POST['idsn'].strip()
            userObjs = User.objects.all().filter(idsn = idsn)
            if userObjs != None and len(userObjs) > 0:
                if eletype == '1':
                    Candidate(eletype = 1, user = userObjs[0], picfile = picfile, sex = sex, birthyear = int(birthyear), \
                              backgroud = backgroud, nation = nation, videourl = videourl, politics = politics, othertext = othertext).save()
                elif eletype == '0':
                    Candidate(eletype = 0, user = userObjs[0], picfile = picfile, sex = sex, birthyear = int(birthyear), \
                              backgroud = backgroud, nation = nation, politics = politics, othertext = othertext).save()
                return msg(request, "mysite:addcandidate", "添加成功")
            else:
                return msg(request, "mysite:addcandidate", "添加失败！请先将候选人注册成选民！")
    form = RegCanditeForm()
    c = {}
    c['form'] = form
    return render_to_response('mysite/addcandidate.html', c, context_instance=RequestContext(request))

@csrf_exempt
def qrycandidates(request, page = 1):
    #todo...
    if chkAdminCookies(request) == None:
        return  msg(request, "mysite:index", "无权限查看！")
    objs = None
    if request.method == 'POST':
        if 'qrytype' in request.POST:
            type = request.POST['qrytype']
            key = request.POST.get('qrykey','')
            objs = getCandidatesObjs(type, key)
            request.session['qrycandidatestype'] = type
            request.session['qrycandidateskey'] = key
        elif 'pagenum' in request.POST:
            objs = getCandidatesObjs(request.session['qrycandidatestype'], request.session['qrycandidateskey'])
            page = request.POST['pagenum']
    c = {'items': getPageContent(page, objs, 1),
         'listurl': 'mysite:qrycandidates',
         'delurl': 'mysite:delcandidate',
         'name': True,
         'eleltype': True,
         'suffix': True,
         'pic': True,
         'del': True,
         'selected' : request.session.get('qrycandidatestype', '')
         }
    return render_to_response('mysite/qrycandidates.html', c, context_instance=RequestContext(request))

@csrf_exempt
def delcandidate(request, id):
    if chkAdminCookies(request) == None:
        return  msg(request, "mysite:index", "无权限查看！")
    Candidate.objects.all().filter(id = id)[0].delete()
    return qrycandidates(request)

@csrf_exempt
def gettext(request, id):
    c = {
        "content": Text.objects.all().filter(id = id)[0].content,
         }
    if id == '0':
        c["navlabel"] = "navtextorg"
    elif id == '1':
        c["navlabel"] = "navtextpln"
    else:
        c["navlabel"] = "navtextpxc"
    return render_to_response('mysite/gettext.html', c, context_instance=RequestContext(request))

@csrf_exempt
def settext(request, id):
    if chkAdminCookies(request) == None:
        return  msg(request, "mysite:index", "无权限查看！")
    if request.method == 'POST':
        form = SetTextForm(request.POST)
        if form.is_valid():
            content = request.POST["content"]
            curObj = Text.objects.all().filter(id = id)[0]
            curObj.content = content
            curObj.save()
        return HttpResponseRedirect(reverse('mysite:gettext',kwargs={'id': id}))
    form = SetTextForm(initial = {"content":Text.objects.all().filter(id = id)[0].content})
    c = {
        "form": form,
        "textid": id,
        "editenb": True,
    }
    if id == '0':
        c['navlabel'] = "navedittextorg"
    elif id == '1' :
        c['navlabel'] = "navedittextpln"
    else:
        c['navlabel'] = "navedittextpxc"
    return render_to_response('mysite/settext.html', c, context_instance=RequestContext(request))

@csrf_exempt
def candidate(request, id):
    #todo...
    obj = Candidate.objects.all().filter(id = id)[0]
    c = {
        "obj":obj,
    }
    return render_to_response('mysite/candidate.html', c, context_instance=RequestContext(request))

@csrf_exempt
def getvotercnt(request):
    return HttpResponse(str(User.objects.all().count()))

@csrf_exempt
def picreg(request):
    if request.method == 'POST':
        form = RegByJudgeForm(request.POST, request.FILES)
        if form.is_valid():
            frontpic = request.FILES['frontpic']
            backpic = request.FILES['backpic']
            idsn = request.POST['idsn']
            type = int(request.POST['type'])
            phone = request.POST['phone']
            username = request.POST['username']
            if len(User.objects.all().filter(idsn = idsn)) == 0 and len(Judge_Queue.objects.all().filter(finished = False).filter(idsn = idsn)) == 0:
                Judge_Queue(idsn = idsn, username = username, phone = phone, type = type, backpic = backpic, frontpic = frontpic).save()
                return msg(request,"mysite:loginpwd","申请提交成功！请等待操作员的审批，审批结果将以短信告知您。")
            else:
                return msg(request,"mysite:picreg","申请提交错误！该用户已经审批登记成功或者您已经提交过申请，请直接进行登录，如果不知道验证码，请联系操作员！")
        else:
            return msg(request,"mysite:picreg","申请格式不规范！请仔细检查！")
    form = RegByJudgeForm()
    documents = Judge_Queue.objects.all()
    return render_to_response(
        'mysite/login.html',
        {'form': form, 'documents': documents, 'picreg':True},
        context_instance=RequestContext(request)
    )


@csrf_exempt
def judge(request):
    if chkAdminCookies(request) == None:
        return msg(request, "mysite:index", "无权限查看！")
    if request.method == 'POST':
        flag = int(request.POST['flag'])
        id = request.POST['id']
        jqObj = Judge_Queue.objects.all().filter(id = id)[0]
        if flag == 1 and jqObj.finished == False:
            if len(User.objects.all().filter(idsn = jqObj.idsn)) == 0:
                User(idsn = jqObj.idsn, username = jqObj.username, phone = jqObj.phone, type = jqObj.type).save()
                jqObj.finished = True
                jqObj.save()
                msg(request, 'mysite:judge', "审核接受成功!")
            else:
                msg(request, 'mysite:judge', "审核出错!")
        elif flag == 0:
            jqObj.delete()
            msg(request, 'mysite:judge', "审核拒绝成功!")
        else:
            msg(request, 'mysite:judge', "审核出错!")
    c = {}
    qryObjs = Judge_Queue.objects.all().filter(finished = False)[:1]
    if len(qryObjs) >= 1:
        c["obj"] = qryObjs[0]

    return render_to_response('mysite/judge.html', c, context_instance=RequestContext(request))



