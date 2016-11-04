# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mission_mapping', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MissionType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=400, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=400, null=True)),
                ('system_type', models.CharField(max_length=200, null=True)),
                ('dependencies', models.ManyToManyField(to='mission_mapping.System', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='mission',
            name='poc',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='serviceinterruption',
            name='poc',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='mission',
            name='description',
            field=models.CharField(max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='mission',
            name='end_time',
            field=models.DateTimeField(null=True, verbose_name='end time'),
        ),
        migrations.AlterField(
            model_name='mission',
            name='start_time',
            field=models.DateTimeField(null=True, verbose_name='start time'),
        ),
        migrations.AlterField(
            model_name='serviceinterruption',
            name='description',
            field=models.CharField(max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='serviceinterruption',
            name='end_time',
            field=models.DateTimeField(null=True, verbose_name='end time'),
        ),
        migrations.AlterField(
            model_name='serviceinterruption',
            name='start_time',
            field=models.DateTimeField(null=True, verbose_name='start time'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(max_length=2, choices=[('MO', 'Mission Planner'), ('SP', 'Service Provider'), ('CS', 'Communications Squadron'), ('AM', 'ASI Manager'), ('ET', 'Enterpise Service Provider')]),
        ),
        migrations.AddField(
            model_name='missiontype',
            name='systems',
            field=models.ManyToManyField(to='mission_mapping.System', null=True),
        ),
        migrations.AddField(
            model_name='mission',
            name='systems',
            field=models.ManyToManyField(to='mission_mapping.System', null=True),
        ),
        migrations.AddField(
            model_name='serviceinterruption',
            name='systems',
            field=models.ManyToManyField(to='mission_mapping.System', null=True),
        ),
    ]
