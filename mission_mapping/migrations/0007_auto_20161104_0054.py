# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mission_mapping', '0006_auto_20161104_0054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='system',
            name='status_description',
            field=models.CharField(default=100, max_length=400, blank=True),
        ),
    ]
