# -*- coding: utf-8 -*-
from django import forms
from datetime import datetime

class LoginForm(forms.Form):
    #username = forms.CharField(max_length = 30)
    idsn = forms.CharField(max_length = 30 )
    #password = forms.CharField(max_length = 30)
    docfile = forms.FileField(
        label = 'Select a pic',
        )

class LoginpwdForm(forms.Form):
    idsn = forms.CharField(widget=forms.TextInput(attrs={ 'size': '25'}), max_length = 30, label = '身份证号')
    pwd = forms.CharField(widget=forms.TextInput(attrs={ 'size': '15'}), max_length=30, label = '验证码')

class RegExlForm(forms.Form):
    docfile = forms.FileField(
        label = '上传表格文件（注意一定要xlsx格式的表格）',
    )

class RegForm(forms.Form):
    username = forms.CharField(max_length = 30, label = "姓名")
    idsn = forms.CharField(max_length = 30, label = '身份证号')
    phone = forms.CharField(max_length = 30, label = '手机号')
    #addr = forms.CharField(max_length = 256)
    #birth = forms.CharField(max_length = 50)
    #sex = forms.CharField(max_length = 10)
    #nation = forms.CharField(max_length = 30)

class SetTextForm(forms.Form):
    content = forms.CharField(widget = forms.Textarea, label = '内容')


class RegCanditeForm(forms.Form):
    ET_CHOICES = [
        (0, '委员'),
        (1, '主任'),
    ]
    eletype = forms.ChoiceField(widget = forms.Select, choices = ET_CHOICES, label = "竞选类型")

    name = forms.CharField(max_length = 30, label = '姓名')

    picfile = forms.FileField(label = "上传头像")

    SEX_CHOICES = [
        ('男', '男'),
        ('女', '女'),
    ]
    sex = forms.ChoiceField(widget = forms.Select, choices = SEX_CHOICES, label = '性别')

    BY_CHOICES = [(str(i), str(i)) for i in range(1935, 2015)]
    birthyear = forms.ChoiceField(widget = forms.Select, choices = BY_CHOICES, label = '出生年份')

    BK_CHOICES= [
        ('小学','小学'),
        ('初中','初中'),
        ('高中','高中'),
        ('职高','职高'),
        ('中专','中专'),
        ('大专','大专'),
        ('技校','技校'),
        ('本科','本科'),
        ('硕士','硕士'),
        ('博士','博士'),
        ('文盲','文盲'),
    ]
    backgroud = forms.ChoiceField(widget = forms.Select, choices = BK_CHOICES, label = '学历')

    N_CHOICES = [
        ("汉族","汉族"),
        ("蒙古族","蒙古族"),
        ("彝族","彝族"),
        ("侗族","侗族"),
        ("哈萨克族","哈萨克族"),
        ("畲族","畲族"),
        ("纳西族","纳西族"),
        ("仫佬族","仫佬族"),
        ("仡佬族","仡佬族"),
        ("怒族","怒族"),
        ("保安族","保安族"),
        ("鄂伦春族","鄂伦春族"),
        ("回族","回族"),
        ("壮族","壮族"),
        ("瑶族","瑶族"),
        ("傣族","傣族"),
        ("高山族","高山族"),
        ("景颇族","景颇族"),
        ("羌族","羌族"),
        ("锡伯族","锡伯族"),
        ("乌孜别克族","乌孜别克族"),
        ("裕固族","裕固族"),
        ("赫哲族","赫哲族"),
        ("藏族","藏族"),
        ("布依族","布依族"),
        ("白族","白族"),
        ("黎族","黎族"),
        ("拉祜族","拉祜族"),
        ("柯尔克孜族","柯尔克孜族"),
        ("布朗族","布朗族"),
        ("阿昌族","阿昌族"),
        ("俄罗斯族","俄罗斯族"),
        ("京族","京族"),
        ("门巴族","门巴族"),
        ("维吾尔族","维吾尔族"),
        ("朝鲜族","朝鲜族"),
        ("土家族","土家族"),
        ("傈僳族","傈僳族"),
        ("水族","水族"),
        ("土族","土族"),
        ("撒拉族","撒拉族"),
        ("普米族","普米族"),
        ("鄂温克族","鄂温克族"),
        ("塔塔尔族","塔塔尔族"),
        ("珞巴族","珞巴族"),
        ("苗族","苗族"),
        ("满族","满族"),
        ("哈尼族","哈尼族"),
        ("佤族","佤族"),
        ("东乡族","东乡族"),
        ("达斡尔族","达斡尔族"),
        ("毛南族","毛南族"),
        ("塔吉克族","塔吉克族"),
        ("德昂族","德昂族"),
        ("独龙族","独龙族"),
        ("基诺族","基诺族"),
    ]
    nation = forms.ChoiceField(widget = forms.Select, choices = N_CHOICES,label = '民族')

    videourl = forms.CharField(max_length = 256, label = '竞选视频URL', required=False)

    # 0群众  1共青团员 2中共预备党员 3中共党员  4民主党派成员
    P_CHOICES = [
        ('群众','群众'),
        ('共青团员','共青团员'),
        ('中共预备党员','中共预备党员'),
        ('中共党员','中共党员'),
        ('民主党派成员','民主党派成员'),
    ]
    politics = forms.ChoiceField(widget = forms.Select, choices = P_CHOICES, label = '政治面貌')

    othertext = forms.CharField(widget = forms.Textarea, label = '其他说明', required=False)


