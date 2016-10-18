from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    email_address = models.CharField(max_length=200)
    ROLES = (
        ("MO", "Mission Owner"),
        ("SP", "Service Provider"),
        ("CS", "Communications Squadron Technician"),
        ("AM", "ASI Manager"),
        ("ET", "Enterpise Service Technician"),
        ("MG", "Manager")
    )
    role = models.CharField(
        max_length=2,
        choices=ROLES
    )

class Mission(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    organization = models.Organization()
    poc = models.POC()
    start_time = models.DateTimeField('start time')
    end_time = models.DateTimeField('end time')
    #cyber terrain

class Organization(models.Model):
    name = models.CharField(max_length=200)

class POC(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    email_address = models.CharField(max_length=200)

class ServiceInterruption(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=400)
    organization = models.Organization()
    poc = models.POC()
    start_time = models.DateTimeField('start time')
    end_time = models.DateTimeField('end time')
    scheduled = models.BooleanField(default=true)

#Cyber terrain
# - consists of devices, systems, has status, %operational,

#Objects:
#   Tree like structure?
#   Network device (type: router, switch)
#   System (types: server, PC)
#   Circuit
