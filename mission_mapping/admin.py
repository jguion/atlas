from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Organization)
admin.site.register(System)
admin.site.register(MissionType)
admin.site.register(Mission)
admin.site.register(ServiceInterruption)
admin.site.register(MissionToMissionAssociation)
admin.site.register(MissionToSystemAssociation)
admin.site.register(SystemToSystemAssociation)
admin.site.register(Vulnerability)
admin.site.register(CVE)
admin.site.register(ThreatActor)
admin.site.register(Threat)
admin.site.register(CyberEvent)
