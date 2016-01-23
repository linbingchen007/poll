# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0002_auto_20151204_2118'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='nation',
            field=models.CharField(default=b'\xe6\xb1\x89\xe6\x97\x8f', max_length=16),
        ),
    ]
