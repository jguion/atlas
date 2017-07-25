# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mission_mapping', '0012_auto_20170719_1747'),
    ]

    operations = [
        migrations.CreateModel(
            name='CyberEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.IntegerField(null=True, choices=[(0, 'Authorized Service Interruption'), (1, 'Unexpected Outage'), (2, 'Denial of Service'), (3, 'Root Level Breach'), (4, 'User Level Breach'), (99, 'Other')])),
                ('description', models.CharField(max_length=1000, null=True, blank=True)),
                ('is_resolved', models.BooleanField(default=False)),
                ('start_time', models.DateTimeField(null=True, verbose_name='start time')),
                ('expected_end_time', models.DateTimeField(null=True, verbose_name='expected end time')),
                ('confidentiality_impact', models.IntegerField(default=0, null=True, choices=[(5, 'Very High'), (4, 'High'), (3, 'Medium'), (2, 'Low'), (1, 'Very Low'), (0, 'None'), (-1, 'Unknown')])),
                ('integrity_impact', models.IntegerField(default=0, null=True, choices=[(5, 'Very High'), (4, 'High'), (3, 'Medium'), (2, 'Low'), (1, 'Very Low'), (0, 'None'), (-1, 'Unknown')])),
                ('availability_impact', models.IntegerField(default=0, null=True, choices=[(5, 'Very High'), (4, 'High'), (3, 'Medium'), (2, 'Low'), (1, 'Very Low'), (0, 'None'), (-1, 'Unknown')])),
                ('system', models.ForeignKey(to='mission_mapping.System')),
            ],
        ),
        migrations.AlterField(
            model_name='serviceinterruption',
            name='criticality',
            field=models.CharField(max_length=1, null=True, choices=[('H', 'High'), ('M', 'Medium'), ('L', 'Low'), ('N', 'None')]),
        ),
    ]
