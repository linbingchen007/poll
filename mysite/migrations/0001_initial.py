# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import mysite.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('pvlevel', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('eletype', models.IntegerField(default=0)),
                ('name', models.CharField(max_length=30)),
                ('picfile', models.FileField(upload_to=mysite.models.candidatepic_path)),
                ('sex', models.BooleanField(default=0)),
                ('birthyear', models.IntegerField(default=0)),
                ('backgroud', models.IntegerField(default=0)),
                ('nation', models.CharField(default=b'\xe6\xb1\x89', max_length=5)),
                ('videourl', models.CharField(max_length=256)),
                ('politics', models.IntegerField(default=0)),
                ('othertext', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('text', models.CharField(max_length=256)),
                ('val', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Choice2',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('text', models.CharField(max_length=256)),
                ('val', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Exl',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('docfile', models.FileField(upload_to=mysite.models.exl_path)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('time', models.DateTimeField(default=datetime.datetime.now, max_length=10, db_index=True)),
                ('action', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Pic',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('date', models.DateTimeField(default=datetime.datetime.now, db_index=True)),
                ('docfile', models.FileField(upload_to=mysite.models.pic_path)),
                ('uid', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('text', models.CharField(max_length=256)),
                ('pollcnt', models.IntegerField(default=0)),
                ('st', models.DateTimeField()),
                ('dt', models.DateTimeField()),
                ('commitcnt', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.CharField(max_length=30)),
                ('idsn', models.CharField(max_length=30, db_index=True)),
                ('addr', models.CharField(max_length=256)),
                ('birth', models.CharField(max_length=50)),
                ('sex', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=20)),
                ('pwd', models.CharField(default=mysite.models.randpwd, max_length=40)),
                ('nation', models.CharField(max_length=30)),
                ('hashsn', models.CharField(max_length=35, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='User_Choice2_Rel',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('choice2', models.ForeignKey(to='mysite.Choice2')),
                ('user', models.ForeignKey(to='mysite.User')),
            ],
        ),
        migrations.CreateModel(
            name='User_Choice_Rel',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('choice', models.ForeignKey(to='mysite.Choice')),
                ('user', models.ForeignKey(to='mysite.User')),
            ],
        ),
        migrations.CreateModel(
            name='User_Question',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('question', models.ForeignKey(to='mysite.Question')),
                ('user', models.ForeignKey(to='mysite.User')),
            ],
        ),
        migrations.CreateModel(
            name='Valid',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('uid', models.CharField(max_length=20, db_index=True)),
                ('key', models.CharField(max_length=33)),
            ],
        ),
        migrations.CreateModel(
            name='Var',
            fields=[
                ('name', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('val', models.CharField(max_length=256)),
            ],
        ),
        migrations.AddField(
            model_name='choice2',
            name='question',
            field=models.ForeignKey(related_name='choices2', to='mysite.Question'),
        ),
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(related_name='choices', to='mysite.Question'),
        ),
    ]
