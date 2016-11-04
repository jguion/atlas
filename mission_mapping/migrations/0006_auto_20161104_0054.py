# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mission_mapping', '0005_auto_20161104_0048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='system',
            name='status',
            field=models.IntegerField(null=True, choices=[(100, 'Fully Operational'), (50, 'Partially Degraded'), (0, 'Non-Operational'), (75, 'HAZCON')]),
        ),
        migrations.AlterField(
            model_name='system',
            name='status_description',
            field=models.CharField(default='FO', max_length=400, blank=True),
        ),
    ]
