# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0002_candidate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Var',
            fields=[
                ('name', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('val', models.CharField(max_length=256)),
            ],
        ),
    ]
