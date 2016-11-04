# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mission_mapping', '0003_auto_20161103_2158'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceinterruption',
            name='pending',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='mission',
            name='description',
            field=models.CharField(max_length=400, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mission',
            name='poc',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
