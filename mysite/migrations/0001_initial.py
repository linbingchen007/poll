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
            name='Choice',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('text', models.CharField(max_length=256)),
                ('val', models.IntegerField(default=0)),
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
                ('st', models.DateTimeField()),
                ('dt', models.DateTimeField()),
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
                ('nation', models.CharField(max_length=30)),
                ('hashsn', models.CharField(max_length=35, db_index=True)),
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
        migrations.AddField(
            model_name='choice',
            name='question',
            field=models.ForeignKey(related_name='choices', to='mysite.Question'),
        ),
    ]
