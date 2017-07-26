from django.shortcuts import get_object_or_404, render
import datetime

from .models import *
import json

from utils import *

# Create your views here.

def dashboard(request):
    context = {}
    return render(request, "index.html", context)

def missions(request):
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    mission_list = Mission.objects.all().filter(end_time__gte=yesterday)
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

        #captures criticality of system to mission
        criticality_dict = {}
        m['status'] = calculate_mission_impact(mission, criticality_dict)
        m['status_description'] = "%s - Impact due to dependencies"%(IMPACT_LIST[m['status']])

        m['risk'] = calculate_mission_risk(mission, criticality_dict)
        m['risk_description'] = "%s - Risk due to dependencies"%(RISK_LIST[m['risk']])

        #Include the system if it is added to the mission or mission type
        systems_set = mission.systems.all()
        systems = []
        mission_risk = 0
        for system in systems_set:
            s = {}
            s['id'] = system.id
            s['name'] = system.name
            s['description'] = system.description
            s['system_type'] = system.system_type
            s['organization'] = system.organization.name
            s['status'] = calculate_system_status(system)
            s['status_description'] = system.status_description
            s['risk'] = calculate_system_risk(system)
            s['criticality'] = IMPACT_LIST[criticality_dict[system.id]]
            systems.append(s)

        m['systems'] = systems

        missions.append(m)

    mission_types = list(MissionType.objects.values("id", "name"))

    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.date) else None
    context = json.dumps({'missions': missions, "mission_types":mission_types}, default=dthandler)
    return render(request, "missions.html", {'context': context})

def add_mission(request):
    context = {}
    return render(request, "missions.html", context)

def mission(request, mission_id):
    mission = get_object_or_404(Mission, pk=mission_id)

    m = {}
    m['id'] = mission.id
    m['name'] = mission.name
    m['description'] = mission.description
    m['organization'] = mission.organization.name
    m['mission_type'] = mission.mission_type.name
    m['start_time'] = mission.start_time
    m['end_time'] = mission.end_time


    criticality_dict = {}
    event_list = []
    m['status'] = calculate_mission_impact(mission, criticality_dict, event_list)
    m['status_description'] = "%s - Impact due to dependencies"%(IMPACT_LIST[m['status']])

    event_table = []
    for (system, event) in event_list:
        e = {}
        e['system_name'] = system.name
        e['event_name'] = event.description
        e['type'] = event.type
        e['confidentiality_impact'] = IMPACT_LIST[event.confidentiality_impact]
        e['integrity_impact'] = IMPACT_LIST[event.integrity_impact]
        e['availability_impact'] = IMPACT_LIST[event.availability_impact]
        event_table.append(e)
    m['event_table'] = event_table

    threat_list = []
    m['risk'] = calculate_mission_risk(mission, criticality_dict, threat_list)
    m['risk_description'] = "%s - Risk due to dependencies"%(RISK_LIST[m['risk']])

    risk_table = []
    for (threat, cve, system) in threat_list:
        r = {}
        r['threat_name'] = threat.name
        r['threat_actor'] = threat.actor.name
        r['targeted_vulnerability'] = cve.name
        r['vulnerability_severity'] = float(cve.severity_score)
        r['system_name'] = system.name
        risk_table.append(r)
    print risk_table
    m['risk_table'] = risk_table

    #Include the system if it is added to the mission or mission type
    systems_set = mission.systems.all()
    systems = []
    nodes = [{
        'id': "M%s"%mission.id,
        'label': "*%s"%mission.name,
        'color': get_impact_color(m['status'])
    }]

    risk_nodes = [{
        'id': "M%s"%mission.id,
        'label': "*%s"%mission.name,
        'color': get_impact_color(m['risk'])
    }]
    edges = []

    visited = set()
    dependencies = set()
    for system in systems_set:
        s = {}
        s['id'] = system.id
        s['name'] = system.name
        s['description'] = system.description
        s['system_type'] = system.system_type
        s['organization'] = system.organization.name
        s['status'] = calculate_system_status(system)
        s['status_description'] = system.status_description
        systems.append(s)

        n = {}
        n['id'] = system.id
        n['label'] = system.name
        n['color'] = get_status_color(calculate_system_status(system))

        nodes.append(n)
        visited.add(system.id)

        r = n.copy()

        r['color'] = get_impact_color(calculate_system_risk(system))
        risk_nodes.append(r)

        e = {}
        e['from'] = "M%s"%mission.id
        e['to'] = system.id
        edges.append(e)
        dependencies = system.dependencies.all()
        for dep in dependencies:
            if dep.id not in visited:
                n = {}
                n['id'] = dep.id
                n['label'] = dep.name
                n['color'] = get_status_color(calculate_system_status(dep))
                nodes.append(n)
                visited.add(dep.id)

                r = n.copy()
                r['color'] = get_impact_color(calculate_system_risk(dep))
                risk_nodes.append(r)

            e = {}
            e['from'] = system.id
            e['to'] = dep.id
            edges.append(e)

        dependencies = set(dependencies)
        while dependencies:
            dep = dependencies.pop()
            if dep.id not in visited:
                n = {}
                n['id'] = dep.id
                n['label'] = dep.name
                n['color'] = get_status_color(calculate_system_status(dep))
                nodes.append(n)
                visited.add(dep.id)

                r = n.copy()
                r['color'] = get_impact_color(calculate_system_risk(dep))
                risk_nodes.append(r)

            for d2 in dep.dependencies.all():
                e = {}
                e['from'] = dep.id
                e['to'] = d2.id
                edges.append(e)

            dependencies = dependencies | set(dep.dependencies.all())
            dependencies = dependencies - visited

    m['systems'] = systems
    m['nodes'] = nodes
    m['risk_nodes'] = risk_nodes
    m['edges'] = edges

    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.date) else None
    context = json.dumps({'mission': m}, default=dthandler)
    return render(request, "mission.html", {'context': context})

def mission_types(request):
    mission_type_list = MissionType.objects.all()

    missions_types = []
    for mt in mission_type_list:
        m = {}
        m['id'] = mt.id
        m['name'] = mt.name
        m['description'] = mt.description
        m['organization'] = mt.organization.name

        systems_set = mt.systems.all()
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
        missions_types.append(m)

    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.date) else None
    context = json.dumps({'mission_types': missions_types}, default=dthandler)
    return render(request, "mission_types.html", {'context': context})

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

def system(request, system_id):
    system = get_object_or_404(System, pk=system_id)
    s = {}
    s['id'] = system.id
    s['name'] = system.name
    s['description'] = system.description
    s['system_type'] = system.system_type
    s['organization'] = system.organization.name
    s['status'] = system.status
    s['status_description'] = system.status_description


    nodes = [{
        'id': system.id,
        'label': "*%s"%system.name
    }]
    edges = []

    visited = set()
    visited.add(system.id)
    dependencies = set()

    dependencies = system.dependencies.all()
    for dep in dependencies:
        n = {}
        n['id'] = dep.id
        n['label'] = dep.name
        n['color'] = get_status_color(dep.status)
        nodes.append(n)
        visited.add(dep.id)

        e = {}
        e['from'] = system.id
        e['to'] = dep.id
        edges.append(e)

    dependencies = set(dependencies)
    while dependencies:
        dep = dependencies.pop()
        if dep.id not in visited:
            n = {}
            n['id'] = dep.id
            n['label'] = dep.name
            n['color'] = get_status_color(dep.status)
            nodes.append(n)
            visited.add(dep.id)

        for d2 in dep.dependencies.all():
            e = {}
            e['from'] = dep.id
            e['to'] = d2.id
            edges.append(e)

        dependencies = dependencies | set(dep.dependencies.all())
        dependencies = dependencies - visited

        s['nodes'] = nodes
        s['edges'] = edges

    dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.date) else None
    context = json.dumps({'system': s}, default=dthandler)
    return render(request, "system.html", {'context': context})

def service_interruption(request):
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    asi_list = ServiceInterruption.objects.all().filter(end_time__gte=yesterday)
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
