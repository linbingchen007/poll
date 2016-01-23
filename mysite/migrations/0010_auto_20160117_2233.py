# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0009_auto_20160117_2212'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='type',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='choice2',
            name='type',
            field=models.IntegerField(default=1),
        ),
    ]
