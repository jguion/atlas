from django.shortcuts import render
import datetime

from .models import *
import json

# Create your views here.

def dashboard(request):
    context = {}
    return render(request, "index.html", context)

def missions(request):
    mission_list = Mission.objects.all()
    #values("name", "description", "organization__name", "mission_type__name", "mission_type__systems", "start_time", "end_time", "systems")
    missions = []
    for mission in mission_list:
        m = {}
        m['id'] = mission.id
        m['name'] = mission.name
        m['description'] = mission.description
        m['organization'] = mission.organization.name
        m['mission_type'] = mission.mission_type.name
        m['start_time'] = mission.start_time
        m['end_time'] = mission.end_time

        systems_set = mission.systems.all() | mission.mission_type.systems.all()
        systems = []
        mission_status = 100
        for system in systems_set:
            s = {}
            s['id'] = system.id
            s['name'] = system.name
            s['description'] = system.description
            s['system_type'] = system.system_type
            s['organization'] = system.organization.name
            s['status'] = system.status
            s['status_description'] = system.status_description
            systems.append(s)

            mission_status = min(mission_status, system.status)
        m['systems'] = systems
        m['status'] = mission_status

        missions.append(m)

    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.date) else None
    context = json.dumps({'missions': missions}, default=dthandler)
    return render(request, "missions.html", {'context': context})

def add_mission(request):
    context = {}
    return render(request, "missions.html", context)

def systems(request):
    systems_list = System.objects.all()
    systems = []
    for system in systems_list:
        s = {}
        s['id'] = system.id
        s['name'] = system.name
        s['description'] = system.description
        s['system_type'] = system.system_type
        s['organization'] = system.organization.name
        s['status'] = system.status
        s['status_description'] = system.status_description

        dependency_set = system.dependencies.all()
        dependencies = []
        for dependency in dependency_set:
            d = {}
            d['id'] = dependency.id
            d['name'] = dependency.name
            d['description'] = dependency.description
            d['system_type'] = system.system_type
            d['organization'] = dependency.organization.name
            d['status'] = dependency.status
            d['status_description'] = dependency.status_description

            dependencies.append(d)

        s['dependencies'] = dependencies
        systems.append(s)

    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.date) else None
    context = json.dumps({'systems':systems}, default=dthandler)
    return render(request, "systems.html", {'context':context})

def service_interruption(request):
    asi_list = ServiceInterruption.objects.all()
    approved_asis = []
    pending_asis = []
    for asi in asi_list:
        a = {}
        a['id'] = asi.id
        a['name'] = asi.name
        a['description'] = asi.description
        a['mission_impact'] = asi.mission_impact
        a['organization'] = asi.organization.name
        a['poc'] = asi.poc
        a['criticality'] = asi.criticality
        a['request_time'] = asi.request_time
        a['start_time'] = asi.start_time
        a['end_time'] = asi.end_time
        a['scheduled'] = asi.scheduled
        a['pending'] = asi.pending

        systems_set = asi.systems.all()
        systems = []
        systems_text = ""
        for system in systems_set:
            if systems_text:
                systems_text += ", "
            s = {}
            s['id'] = system.id
            s['name'] = system.name
            systems_text += system.name
            s['description'] = system.description
            s['system_type'] = system.system_type
            s['organization'] = system.organization.name
            s['status'] = system.status
            s['status_description'] = system.status_description
            systems.append(s)
        a['systems'] = systems
        a['systems_text'] = systems_text

        pending_asis.append(a) if asi.pending else approved_asis.append(a)

    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.date) else None
    context = json.dumps({'approved_asis':approved_asis, 'pending_asis':pending_asis}, default=dthandler)

    return render(request, "service_interruptions.html", {'context':context})
