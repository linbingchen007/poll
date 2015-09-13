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
from datetime import datetime
from mysite.forms import LoginForm, RegForm 
from mysite.models import User, Admin, Pic, Question, User_Choice_Rel, User_Question, Valid
import md5

def init(request):
    #删除数据库所有数据
    Pic.objects.all().delete()
    User.objects.all().delete()
    Valid.objects.all().delete()
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
    valids = Valid.objects.all().filter(uid = uid)
    if len(valids) >= 1:
        if valids[0].key == key:
            return HttpResponse("ok!")
    return HttpResponse("fail!")


@csrf_exempt
def reg(request):
    #注册用户
    #对应的网页模版地址为 mysite/templates/mysite/reg.html
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



