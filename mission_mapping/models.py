from __future__ import unicode_literals

from django.db import models

# Create your models here.

STATUSES = (
    (100, "Fully Operational"),
    (50, "Partially Degraded"),
    (0, "Non-Operational"),
    (75, "HAZCON"),
)

RISKS = (
    (5, "Very High"),
    (4, "High"),
    (3, "Medium"),
    (2, "Low"),
    (1, "Very Low"),
    (0, "Unknown"),
)

CRITICALITY = (
    ('H', "High"),
    ('M', "Medium"),
    ('L', "Low"),
)

class User(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    email_address = models.CharField(max_length=200)
    ROLES = (
        ("MO", "Mission Planner"),
        ("SP", "Service Provider"),
        ("CS", "Communications Squadron"),
        ("AM", "ASI Manager"),
        ("ET", "Enterpise Service Provider")
    )
    role = models.CharField(
        max_length=2,
        choices=ROLES
    )

class Organization(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class POC(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    email_address = models.CharField(max_length=200)
    organization = models.ForeignKey(Organization, null=True)

class System(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400, null=True)
    system_type = models.CharField(max_length=200, null=True)
    organization = models.ForeignKey(Organization, null=True)
    dependencies = models.ManyToManyField("System", blank=True)
    status = models.IntegerField(
        choices=STATUSES,
        null=True
    )
    status_description = models.CharField(max_length=400, default=100, blank=True)

    risk = models.IntegerField(
        choices=RISKS,
        default=0,
        null=True
    )
    risk_description = models.CharField(max_length=400, default="", blank=True)
    vulnerabilities = models.ManyToManyField("Vulnerability", blank=True)

    def __str__(self):
        return self.name

class MissionType(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400, null=True)
    organization = models.ForeignKey(Organization, null=True)
    systems = models.ManyToManyField("System", blank=True)

    def __str__(self):
        return self.name

class Mission(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400, null=True, blank=True)
    organization = models.ForeignKey(Organization, null=True)
    poc = models.CharField(max_length=200, null=True, blank=True)
    mission_type = models.ForeignKey(MissionType, null=True)
    start_time = models.DateTimeField('start time', null=True)
    end_time = models.DateTimeField('end time', null=True)
    #cyber terrain
    systems = models.ManyToManyField("System", blank=True)
    #mission_decomposition
    missions = models.ManyToManyField("Mission", blank=True)
    risk = models.IntegerField(
        choices=RISKS,
        default=0,
        null=True
    )

    def __str__(self):
        return self.name


class ServiceInterruption(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400, null=True)
    mission_impact = models.CharField(max_length=400, null=True)
    organization = models.ForeignKey(Organization, null=True)
    poc = models.CharField(max_length=200, null=True)
    criticality = models.CharField(
        max_length=1,
        choices=CRITICALITY,
        null=True
    )
    request_time = models.DateTimeField('request time', null=True)
    start_time = models.DateTimeField('start time', null=True)
    end_time = models.DateTimeField('end time', null=True)
    scheduled = models.BooleanField(default=True)
    pending = models.BooleanField(default=True)
    systems = models.ManyToManyField("System", blank=True)
    #affected_devices = models.ManyToManyField(NetworkDevice)
    #cyber terrain

    def __str__(self):
        return self.name

class MissionToMissionAssociation(models.Model):
    parent = models.ForeignKey(Mission, related_name='parent')
    child = models.ForeignKey(Mission, related_name='child')
    criticality = models.IntegerField(
        choices=RISKS,
        default=0
    )
class MissionToSystemAssociation(models.Model):
    parent = models.ForeignKey(Mission)
    child = models.ForeignKey(System)
    criticality = models.IntegerField(
        choices=RISKS,
        default=0
    )
class SystemToSystemAssociation(models.Model):
    parent = models.ForeignKey(System, related_name='parent')
    child = models.ForeignKey(System, related_name='child')
    criticality = models.IntegerField(
        choices=RISKS,
        default=0
    )

class CVE(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000, blank=True, null=True)
    severity_score = models.DecimalField(max_digits=3, decimal_places=1)
    impact_score = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    exploitability_score = models.DecimalField(max_digits=3, decimal_places=1, null=True)

    def __str__(self):
        return self.name


class Vulnerability(models.Model):
    cve = models.ForeignKey(CVE)
    description = models.CharField(max_length=1000, null=True)
    severity_score = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    impact_score = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    exploitability_score = models.DecimalField(max_digits=3, decimal_places=1, null=True)

    def __str__(self):
        return self.cve

class ThreatActor(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Threat(models.Model):
    name = models.CharField(max_length=200, null=True)
    actor = models.ForeignKey(ThreatActor)
    targeted_vulnerabilities = models.ManyToManyField("CVE", blank=True)
    targeted_systems = models.ManyToManyField("System", blank=True)
    targeted_organizations = models.ManyToManyField("Organization", blank=True)
    target_description = models.CharField(max_length=1000, blank=True, null=True)
    active = models.BooleanField(default=True)
    start_date = models.DateField('start date', blank=True, null=True)
    end_date = models.DateField('end date', blank=True, null=True)

    def __str__(self):
        return self.name





#class SystemStatus(models.Model):
#    system = models.ForeignKey(System)
#    status = models.IntegerField(null=True)
#    status_description = models.CharField(max_length=400, null=True)
#    date = models.DateTimeField('time', null=True)

#class InterruptionAffectedSystems
#    ASI =

#Cyber terrain
# - consists of devices, systems, has status, %operational,

#Objects:
#   Tree like structure?
#   Network device (type: router, switch)
#   System (types: server, PC)
#   Circuit
