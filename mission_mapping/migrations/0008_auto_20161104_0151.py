# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mission_mapping', '0007_auto_20161104_0054'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceinterruption',
            name='criticality',
            field=models.CharField(max_length=1, null=True, choices=[('H', 'High'), ('M', 'Medium'), ('L', 'Low')]),
        ),
        migrations.AddField(
            model_name='serviceinterruption',
            name='mission_impact',
            field=models.CharField(max_length=400, null=True),
        ),
        migrations.AddField(
            model_name='serviceinterruption',
            name='request_time',
            field=models.DateTimeField(null=True, verbose_name='request time'),
        ),
    ]
