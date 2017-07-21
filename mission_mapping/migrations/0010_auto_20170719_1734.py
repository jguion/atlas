# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mission_mapping', '0009_auto_20170712_1738'),
    ]

    operations = [
        migrations.CreateModel(
            name='CVE',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('severity_score', models.DecimalField(max_digits=3, decimal_places=1)),
                ('impact_score', models.DecimalField(null=True, max_digits=3, decimal_places=1)),
                ('exploitability_score', models.DecimalField(null=True, max_digits=3, decimal_places=1)),
            ],
        ),
        migrations.CreateModel(
            name='MissionToMissionAssociation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('criticality', models.IntegerField(default=0, choices=[(5, 'Very High'), (4, 'High'), (3, 'Medium'), (2, 'Low'), (1, 'Very Low'), (0, 'Unknown')])),
            ],
        ),
        migrations.CreateModel(
            name='MissionToSystemAssociation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('criticality', models.IntegerField(default=0, choices=[(5, 'Very High'), (4, 'High'), (3, 'Medium'), (2, 'Low'), (1, 'Very Low'), (0, 'Unknown')])),
                ('child', models.ForeignKey(to='mission_mapping.System')),
            ],
        ),
        migrations.CreateModel(
            name='SystemToSystemAssociation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('criticality', models.IntegerField(default=0, choices=[(5, 'Very High'), (4, 'High'), (3, 'Medium'), (2, 'Low'), (1, 'Very Low'), (0, 'Unknown')])),
                ('child', models.ForeignKey(related_name='child', to='mission_mapping.System')),
                ('parent', models.ForeignKey(related_name='parent', to='mission_mapping.System')),
            ],
        ),
        migrations.CreateModel(
            name='Threat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('target_description', models.CharField(max_length=1000, null=True)),
                ('active', models.BooleanField(default=True)),
                ('start_date', models.DateField(null=True, verbose_name='start date')),
                ('end_date', models.DateField(null=True, verbose_name='end date')),
            ],
        ),
        migrations.CreateModel(
            name='ThreatActor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Vulnerability',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=1000, null=True)),
                ('severity_score', models.DecimalField(null=True, max_digits=3, decimal_places=1)),
                ('impact_score', models.DecimalField(null=True, max_digits=3, decimal_places=1)),
                ('exploitability_score', models.DecimalField(null=True, max_digits=3, decimal_places=1)),
                ('cve', models.ForeignKey(to='mission_mapping.CVE')),
            ],
        ),
        migrations.AddField(
            model_name='mission',
            name='risk',
            field=models.IntegerField(default=0, null=True, choices=[(5, 'Very High'), (4, 'High'), (3, 'Medium'), (2, 'Low'), (1, 'Very Low'), (0, 'Unknown')]),
        ),
        migrations.AlterField(
            model_name='serviceinterruption',
            name='systems',
            field=models.ManyToManyField(to='mission_mapping.System', blank=True),
        ),
        migrations.AddField(
            model_name='threat',
            name='actor',
            field=models.ForeignKey(to='mission_mapping.ThreatActor'),
        ),
        migrations.AddField(
            model_name='threat',
            name='targeted_organizations',
            field=models.ManyToManyField(to='mission_mapping.Organization', blank=True),
        ),
        migrations.AddField(
            model_name='threat',
            name='targeted_systems',
            field=models.ManyToManyField(to='mission_mapping.System', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='threat',
            name='targeted_vulnerabilities',
            field=models.ManyToManyField(to='mission_mapping.CVE', blank=True),
        ),
        migrations.AddField(
            model_name='missiontosystemassociation',
            name='parent',
            field=models.ForeignKey(to='mission_mapping.Mission'),
        ),
        migrations.AddField(
            model_name='missiontomissionassociation',
            name='child',
            field=models.ForeignKey(related_name='child', to='mission_mapping.Mission'),
        ),
        migrations.AddField(
            model_name='missiontomissionassociation',
            name='parent',
            field=models.ForeignKey(related_name='parent', to='mission_mapping.Mission'),
        ),
        migrations.AddField(
            model_name='system',
            name='vulnerabilities',
            field=models.ManyToManyField(to='mission_mapping.Vulnerability', null=True, blank=True),
        ),
    ]
