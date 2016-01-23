# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mysite.models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0011_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='Judge_Queue',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.CharField(max_length=30, db_index=True)),
                ('type', models.IntegerField(default=0, db_index=True)),
                ('idsn', models.CharField(max_length=30, db_index=True)),
                ('phone', models.CharField(max_length=20)),
                ('frontpic', models.FileField(upload_to=mysite.models.frontpic_path)),
                ('backpic', models.FileField(upload_to=mysite.models.backpic_path)),
            ],
        ),
    ]
