# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0002_auto_20150802_1950'),
    ]

    operations = [
        migrations.AddField(
            model_name='pic',
            name='uid',
            field=models.IntegerField(default=0),
        ),
    ]
