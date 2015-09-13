# -*- coding: utf-8 -*-
from django import forms


class LoginForm(forms.Form):
    #username = forms.CharField(max_length = 30)
    idsn = forms.CharField(max_length = 30 )
    #password = forms.CharField(max_length = 30)
    docfile = forms.FileField(
        label = 'Select a pic',
        )

class RegForm(forms.Form):
    username = forms.CharField(max_length = 30)
    idsn = forms.CharField(max_length = 30)
    #addr = forms.CharField(max_length = 256)
    #birth = forms.CharField(max_length = 50)
    #sex = forms.CharField(max_length = 10)
    #nation = forms.CharField(max_length = 30)
    

