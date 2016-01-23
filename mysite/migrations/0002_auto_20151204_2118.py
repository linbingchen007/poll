# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='backgroud',
            field=models.CharField(default=b'\xe5\xb0\x8f\xe5\xad\xa6', max_length=8),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='nation',
            field=models.CharField(default=b'\xe6\xb1\x89\xe6\x97\x8f', max_length=12),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='politics',
            field=models.CharField(default=b'\xe7\xbe\xa4\xe4\xbc\x97', max_length=12),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='sex',
            field=models.CharField(default=b'\xe7\x94\xb7', max_length=6),
        ),
    ]
