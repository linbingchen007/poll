# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0004_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Counter',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('value', models.IntegerField()),
            ],
            options={
                'db_table': 'counter',
                'managed': False,
            },
        ),
    ]
