# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mission_mapping', '0002_auto_20161103_2131'),
    ]

    operations = [
        migrations.AddField(
            model_name='mission',
            name='mission_type',
            field=models.ForeignKey(to='mission_mapping.MissionType', null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='organization',
            field=models.ForeignKey(to='mission_mapping.Organization', null=True),
        ),
        migrations.AddField(
            model_name='missiontype',
            name='organization',
            field=models.ForeignKey(to='mission_mapping.Organization', null=True),
        ),
        migrations.AddField(
            model_name='poc',
            name='organization',
            field=models.ForeignKey(to='mission_mapping.Organization', null=True),
        ),
        migrations.AddField(
            model_name='serviceinterruption',
            name='organization',
            field=models.ForeignKey(to='mission_mapping.Organization', null=True),
        ),
        migrations.AddField(
            model_name='system',
            name='organization',
            field=models.ForeignKey(to='mission_mapping.Organization', null=True),
        ),
        migrations.AlterField(
            model_name='mission',
            name='systems',
            field=models.ManyToManyField(to='mission_mapping.System', blank=True),
        ),
        migrations.AlterField(
            model_name='missiontype',
            name='systems',
            field=models.ManyToManyField(to='mission_mapping.System', blank=True),
        ),
        migrations.AlterField(
            model_name='serviceinterruption',
            name='systems',
            field=models.ManyToManyField(to='mission_mapping.System', null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='system',
            name='dependencies',
            field=models.ManyToManyField(to='mission_mapping.System', blank=True),
        ),
    ]
