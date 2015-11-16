# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mysite.models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('picfile', models.FileField(upload_to=mysite.models.candidatepic_path)),
                ('videourl', models.CharField(max_length=256)),
                ('profile', models.TextField()),
                ('votetext', models.TextField()),
                ('eletype', models.IntegerField(default=0)),
            ],
        ),
    ]
