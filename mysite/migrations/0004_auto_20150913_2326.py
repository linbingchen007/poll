# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0003_pic_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pic',
            name='uid',
            field=models.CharField(max_length=20),
        ),
    ]
