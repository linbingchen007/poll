# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mysite.models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0006_exl'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='pwd',
            field=models.CharField(default=mysite.models.randpwd, max_length=40),
        ),
    ]
