# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from mysite import views

#url和view.py中的函数进行关联
urlpatterns = patterns('',
                    url(r'^init$', views.init, name='init'),
                    url(r'^login$', views.login, name='login'),
                    #url(r'valid/(?P<key>[^/]+)/(?P<uid>\d+)$',views.valid,name='valid'),
                    url(r'^reg$', views.reg, name='reg'),
                    url(r'^regexl$', views.regexl, name='regexl'),
                    url(r'^admin$', views.admin, name='admin'),
                    url(r'^createpoll$', views.createpoll, name='createpoll'),
                    url(r'^candidates$', views.candidates, name='candidates'),
                    #url(r'editcandidates$',views.editcandidates, name='editcandidates'),
                    url(r'^getauthkey$', views.getauthkey, name='getauthkey'),
                    url(r'^gopagevoters$', views.gopagevoters, name='gopagevoters'),
                    url(r'^getseed$', views.getseed, name='getseed'),
                    url(r'^bind$', views.bind, name='bind'),
                    url(r'^auth/(?P<key>[0-9]+)/(?P<value>[^/]+)$', views.auth, name='auth'),
                    url(r'^voters/(?P<page>[0-9]+)$', views.voters, name='voters'),
                    url(r'^voters$', views.voters, name='voters'),
                    url(r'^qryvoters/(?P<page>[0-9]+)$', views.qryvoters, name='qryvoters'),
                    url(r'^qryvoters$', views.qryvoters, name='qryvoters'),
                    url(r'^delvoter/(?P<idsn>[0-9]+)$', views.delvoter, name='delvoter'),
                    url(r'^poll/(?P<topicid>[^/]+)$', views.poll, name='poll'),
                    url(r'^polls/(?P<type>[^/]+)(/(?P<key>[^/]+)/(?P<uid>\d+))?$', views.polls, name='polls'),
                    url(r'^pollvote/(?P<topicid>[^/]+)/(?P<optid>[^/]+)$', views.pollvote, name='pollvote'),
                       )
