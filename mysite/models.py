from django.db import models
from datetime import datetime

# Create your models here.
def pic_path(instance,filename):
    return '{0}.jpg'.format(str(datetime.now()).replace(':','.'))

class Pic(models.Model):
    id = models.AutoField(primary_key = True)
    date = models.DateTimeField(db_index = True, default=datetime.now)
    docfile = models.FileField(upload_to = pic_path)
    uid = models.CharField(max_length = 20)
   
class User(models.Model):
    id = models.AutoField(primary_key = True)
    username = models.CharField(max_length = 30)
    idsn = models.CharField(db_index = True, max_length = 30)
    addr = models.CharField(max_length = 256)
    birth = models.CharField(max_length = 50)
    sex = models.CharField(max_length = 10)
    #True female False male
    nation = models.CharField(max_length = 30)
    hashsn = models.CharField(db_index = True, max_length = 35)
class Question(models.Model):
    id = models.AutoField(primary_key = True)
    text = models.CharField(max_length = 256)
    st = models.DateTimeField()
    dt = models.DateTimeField()

   
class Choice(models.Model):
    id = models.AutoField(primary_key = True)
    question = models.ForeignKey(Question, related_name='choices')
    text = models.CharField(max_length = 256)
    val = models.IntegerField(default = 0)

class User_Choice_Rel(models.Model):
    id = models.AutoField(primary_key = True)
    user = models.ForeignKey(User)
    choice = models.ForeignKey(Choice)

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

    
    

