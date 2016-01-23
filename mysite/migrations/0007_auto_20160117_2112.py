# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0006_auto_20160117_2035'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidate',
            name='name',
        ),
        migrations.AddField(
            model_name='candidate',
            name='user',
            field=models.ForeignKey(default=2, to='mysite.User'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='suffix',
            field=models.CharField(default=b'', max_length=6, db_index=True),
        ),
    ]
