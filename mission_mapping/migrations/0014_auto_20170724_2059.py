# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mission_mapping', '0013_auto_20170724_1530'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='system',
            name='vulnerabilities',
        ),
        migrations.AddField(
            model_name='vulnerability',
            name='system',
            field=models.ForeignKey(to='mission_mapping.System', null=True),
        ),
        migrations.AlterField(
            model_name='mission',
            name='mission_type',
            field=models.ForeignKey(blank=True, to='mission_mapping.MissionType', null=True),
        ),
        migrations.AlterField(
            model_name='vulnerability',
            name='exploitability_score',
            field=models.DecimalField(null=True, max_digits=3, decimal_places=1, blank=True),
        ),
        migrations.AlterField(
            model_name='vulnerability',
            name='impact_score',
            field=models.DecimalField(null=True, max_digits=3, decimal_places=1, blank=True),
        ),
        migrations.AlterField(
            model_name='vulnerability',
            name='severity_score',
            field=models.DecimalField(null=True, max_digits=3, decimal_places=1, blank=True),
        ),
    ]
