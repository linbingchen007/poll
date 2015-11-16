# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0003_var'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('time', models.DateTimeField(default=datetime.datetime.now, max_length=10, db_index=True)),
                ('action', models.CharField(max_length=256)),
            ],
        ),
    ]
