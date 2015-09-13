# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from mysite import views

#url和view.py中的函数进行关联
urlpatterns = patterns('',
                    url(r'init$', views.init, name='init'),
                    url(r'login$', views.login, name='login'),
                    url(r'valid/(?P<key>[^/]+)/(?P<uid>\d+)$',views.valid,name='valid'),
                    url(r'reg$', views.reg, name='reg'),
                       )
