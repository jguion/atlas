# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mission_mapping', '0010_auto_20170719_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='system',
            name='vulnerabilities',
            field=models.ManyToManyField(to='mission_mapping.Vulnerability', blank=True),
        ),
        migrations.AlterField(
            model_name='threat',
            name='targeted_systems',
            field=models.ManyToManyField(to='mission_mapping.System', blank=True),
        ),
    ]
