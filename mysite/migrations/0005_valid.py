# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0004_auto_20150913_2326'),
    ]

    operations = [
        migrations.CreateModel(
            name='Valid',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('uid', models.CharField(max_length=20, db_index=True)),
                ('key', models.CharField(max_length=33)),
            ],
        ),
    ]
