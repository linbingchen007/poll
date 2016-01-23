# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0007_auto_20160117_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='text',
            field=models.ForeignKey(to='mysite.User'),
        ),
        migrations.AlterField(
            model_name='choice2',
            name='text',
            field=models.ForeignKey(to='mysite.User'),
        ),
    ]
