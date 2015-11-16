# -*- coding: utf-8 -*-
from django import forms


class LoginForm(forms.Form):
    #username = forms.CharField(max_length = 30)
    idsn = forms.CharField(max_length = 30 )
    #password = forms.CharField(max_length = 30)
    docfile = forms.FileField(
        label = 'Select a pic',
        )

class RegExlForm(forms.Form):
    docfile = forms.FileField(
        label = '上传表格文件（注意一定要xlsx格式的表格）',
    )

class RegForm(forms.Form):
    username = forms.CharField(max_length = 30, label = "姓名")
    idsn = forms.CharField(max_length = 30, label = '身份证号')
    #addr = forms.CharField(max_length = 256)
    #birth = forms.CharField(max_length = 50)
    #sex = forms.CharField(max_length = 10)
    #nation = forms.CharField(max_length = 30)

class AdminForm(forms.Form):
    username = forms.CharField(max_length = 30, label = '用户名')
    password = forms.CharField(max_length = 30, label = '密码')



    

