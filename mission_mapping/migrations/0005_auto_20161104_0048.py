# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mission_mapping', '0004_auto_20161103_2217'),
    ]

    operations = [
        migrations.AddField(
            model_name='system',
            name='status',
            field=models.CharField(max_length=2, null=True, choices=[('FO', 'Fully Operational'), ('PD', 'Partially Degraded'), ('NO', 'Non-Operational'), ('HC', 'HAZCON')]),
        ),
        migrations.AddField(
            model_name='system',
            name='status_description',
            field=models.CharField(max_length=400, null=True),
        ),
    ]
