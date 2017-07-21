# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mission_mapping', '0008_auto_20161104_0151'),
    ]

    operations = [
        migrations.AddField(
            model_name='mission',
            name='missions',
            field=models.ManyToManyField(to='mission_mapping.Mission', blank=True),
        ),
        migrations.AddField(
            model_name='system',
            name='risk',
            field=models.IntegerField(default=0, null=True, choices=[(5, 'Very High'), (4, 'High'), (3, 'Medium'), (2, 'Low'), (1, 'Very Low'), (0, 'Unknown')]),
        ),
        migrations.AddField(
            model_name='system',
            name='risk_description',
            field=models.CharField(default='', max_length=400, blank=True),
        ),
    ]
