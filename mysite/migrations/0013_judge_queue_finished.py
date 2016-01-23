# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0012_judge_queue'),
    ]

    operations = [
        migrations.AddField(
            model_name='judge_queue',
            name='finished',
            field=models.BooleanField(default=False, db_index=True),
        ),
    ]
