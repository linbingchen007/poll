# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
import random,string
# Create your models here.
def pic_path(instance, filename):
    return '{0}.jpg'.format(str(datetime.now()).replace(':','.'))

def exl_path(instance, filename):
    return "target.xlsx"

def frontpic_path(instance, filename):
    return 'frontpic/{0}.jpg'.format(str(datetime.now()).replace(':','.'))

def backpic_path(instance, filename):
    return 'backpic/{0}.jpg'.format(str(datetime.now()).replace(':','.'))

def candidatepic_path(instance, filename):
    return 'candidate/{0}.jpg'.format(str(datetime.now()).replace(':','.'))

def randpwd():
    return ''.join(random.SystemRandom().choice(string.digits) for _ in range(10))

class Pic(models.Model):
    id = models.AutoField(primary_key = True)
    date = models.DateTimeField(db_index = True, default=datetime.now)
    docfile = models.FileField(upload_to = pic_path , blank=True, null=True)
    uid = models.CharField(max_length = 20)

class Exl(models.Model):
    id = models.AutoField(primary_key = True)
    docfile = models.FileField(upload_to=exl_path)
   
class User(models.Model):
    id = models.AutoField(primary_key = True)
    username = models.CharField(max_length = 30, db_index=True)
    #0当地居住选民  1外地居住选民 2非本村户籍选民
    type = models.IntegerField(default=0, db_index=True)
    #身份证号
    idsn = models.CharField(db_index = True, max_length = 30)
    addr = models.CharField(max_length = 256)
    birth = models.CharField(max_length = 50)
    suffix = models.CharField(max_length = 6, db_index=True, default = "")
    sex = models.CharField(max_length = 10)
    phone = models.CharField(max_length = 20)
    pwd = models.CharField(max_length=40, default = randpwd)
    #True female False male
    nation = models.CharField(max_length = 30)
    #密钥
    hashsn = models.CharField(db_index = True, max_length = 35)

class Question(models.Model):
    id = models.AutoField(primary_key = True)
    text = models.CharField(max_length = 256)
    pollcnt = models.IntegerField(default=0)
    st = models.DateTimeField()
    dt = models.DateTimeField()
    commitcnt = models.IntegerField(default = 1)

   
class Choice(models.Model):
    id = models.AutoField(primary_key = True)
    question = models.ForeignKey(Question, related_name='choices')
    text = models.ForeignKey(User)
    type =  models.IntegerField(default = 1)  # 0candidate 1optional
    val = models.IntegerField(default = 0)

class Choice2(models.Model):
    id = models.AutoField(primary_key = True)
    question = models.ForeignKey(Question, related_name='choices2')
    text = models.ForeignKey(User)
    type = models.IntegerField(default = 1)  # 0candidate 1optional
    val = models.IntegerField(default = 0)

class User_Choice_Rel(models.Model):
    id = models.AutoField(primary_key = True)
    user = models.ForeignKey(User)
    choice = models.ForeignKey(Choice)

class User_Choice2_Rel(models.Model):
    id = models.AutoField(primary_key = True)
    user = models.ForeignKey(User)
    choice2 = models.ForeignKey(Choice2)

class User_Question(models.Model):
    id = models.AutoField(primary_key = True)
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)

class Admin(models.Model):
    id = models.AutoField(primary_key = True)
    username = models.CharField(max_length = 30)
    password = models.CharField(max_length = 30)
    pvlevel = models.IntegerField(default = 0)

class Valid(models.Model):
    id = models.AutoField(primary_key = True)
    uid = models.CharField(db_index = True, max_length = 20)
    key = models.CharField(max_length = 33)

class Candidate(models.Model):
    id = models.AutoField(primary_key = True)
    # 0 委员 1 主任
    eletype = models.IntegerField(default = 0)
    user = models.ForeignKey(User)
    picfile = models.FileField(upload_to = candidatepic_path)
    sex = models.CharField(max_length = 6, default = "男")
    birthyear = models.IntegerField(default = 0)
    backgroud = models.CharField(max_length = 8, default = "小学")
    nation = models.CharField(max_length = 16, default = "汉族")
    videourl = models.CharField(max_length = 256)
    politics = models.CharField(max_length = 12, default = "群众")
    othertext = models.TextField()


class Var(models.Model):
    name = models.CharField(max_length = 10, primary_key = True)
    val = models.CharField(max_length = 256)

class Log(models.Model):
    id = models.AutoField(primary_key = True)
    time = models.DateTimeField(max_length = 10, db_index = True, default=datetime.now)
    action = models.CharField(max_length = 256)

class Text(models.Model):
    id = models.IntegerField(primary_key = True)
    content = models.TextField()

class Judge_Queue(models.Model):
    id = models.AutoField(primary_key = True)
    username = models.CharField(max_length = 30, db_index=True)
    #0当地居住选民  1外地居住选民 2非本村户籍选民
    type = models.IntegerField(default=0, db_index=True)
    idsn = models.CharField(db_index = True, max_length = 30)
    phone = models.CharField(max_length = 20)
    frontpic = models.FileField(upload_to = frontpic_path)
    backpic =  models.FileField(upload_to = backpic_path)
    finished = models.BooleanField(default=False, db_index=True)











