# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mysite.models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0008_auto_20160117_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pic',
            name='docfile',
            field=models.FileField(null=True, upload_to=mysite.models.pic_path, blank=True),
        ),
    ]
