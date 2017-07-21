# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mission_mapping', '0011_auto_20170719_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='cve',
            name='description',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='threat',
            name='name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='threat',
            name='end_date',
            field=models.DateField(null=True, verbose_name='end date', blank=True),
        ),
        migrations.AlterField(
            model_name='threat',
            name='start_date',
            field=models.DateField(null=True, verbose_name='start date', blank=True),
        ),
        migrations.AlterField(
            model_name='threat',
            name='target_description',
            field=models.CharField(max_length=1000, null=True, blank=True),
        ),
    ]
