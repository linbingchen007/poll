# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mysite.models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0005_user_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exl',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('docfile', models.FileField(upload_to=mysite.models.exl_path)),
            ],
        ),
    ]
