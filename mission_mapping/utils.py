from .models import *
import math

#Status
FULLY_OPERATIONAL = 100
MINOR_DEGRADATION = 75
PARTUAL_DEGRADATION = 50
MAJOR_DEGRADATION = 25
NON_OPERATIONAL = 0

#impact_score
VERY_HIGH = 5
HIGH = 4
MEDIUM = 3
LOW = 2
VERY_LOW = 1
NONE = 0

IMPACT_LIST = ["None", "Very Low", "Low", "Medium", "High", "Very High"]
RISK_LIST = ["Unknown", "Very Low", "Low", "Medium", "High", "Very High"]

#Status / Mission Impact
# X         | N | VL | L  | M  | H  | VH
#___________________________________
# Non Op    | N | L  | M  | H  | VH | VH
# Major     | N | L  | M  | H  | H  | VH
# Medium    | N | VL | L  | M  | H  | H
# Minor     | N | VL | VL | L  | L  | M
# Fully Op  | N | N  | N  | N  | N  | N

MISSION_IMPACT_DICT = [
    [0, 2, 3, 4, 5, 5],
    [0, 2, 3, 4, 4, 5],
    [0, 1, 2, 3, 4, 4],
    [0, 1, 2, 3, 4, 4],
    [0, 1, 1, 2, 2, 3],
    [0, 0, 0, 0, 0, 0],
]

#Risk / Mission Impact
# X    | UNK | VL | L  | M  | H  | VH
#___________________________________
# UNK  | UNK | UNK| UNK| UNK| UNK| UNK
# VL   | UNK | VL | VL | VL | L  | L
# L    | UNK | VL | L  | L  | L  | M
# M    | UNK | VL | L  | M  | M  | H
# H    | UNK | VL | L  | M  | H  | VH
# VH   | UNK | VL | L  | M  | H  | VH

MISSION_RISK_DICT = [
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 2, 2],
    [0, 1, 2, 2, 2, 3],
    [0, 1, 2, 3, 3, 4],
    [0, 1, 2, 3, 4, 5],
    [0, 1, 2, 3, 4, 5],
]

# Threat / Vulnerability
# X    | UNK | VL | L  | M  | H  | VH
#___________________________________
# UNK  | UNK | UNK| UNK| UNK| UNK| UNK
# VL   | UNK | VL | VL | L  | L  | M
# L    | UNK | VL | L  | L  | M  | M
# M    | UNK | L  | L  | M  | M  | H
# H    | UNK | L  | M  | M  | H  | H
# VH   | UNK | M  | M  | H  | H  | VH

LIKELIHOOD_RISK_DICT = [
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 2, 2, 3],
    [0, 1, 2, 2, 3, 3],
    [0, 2, 2, 3, 3, 4],
    [0, 2, 3, 3, 4, 4],
    [0, 3, 3, 4, 4, 5],
]

#Helper methods
def get_status_color(status):
    if status >= FULLY_OPERATIONAL:
        return 'rgb(131, 217, 116)' #green
    elif status >= PARTUAL_DEGRADATION:
        return 'rgb(255, 201, 70)' #yellow
    else:
        return 'rgb(241, 138, 114)' #red

def get_impact_color(impact):
    if impact <= 1:
        return 'rgb(131, 217, 116)'
    elif impact <= 3:
        return 'rgb(255, 201, 70)'
    else:
        return 'rgb(241, 138, 114)'

def impact_to_status_translation(impact):
    status = FULLY_OPERATIONAL
    if impact > 4:
        status = NON_OPERATIONAL
    elif impact > 3:
        status = PARTUAL_DEGRADATION
    elif impact > 1:
        status = MINOR_DEGRADATION
    return status

def get_system_status(system, events, event_list=[]):
    if not events:
        return FULLY_OPERATIONAL
    impact_level = 0
    for event in events:
        impact_level = max(event.confidentiality_impact, event.integrity_impact, event.availability_impact)
        event_list.append((system, event))
    return impact_to_status_translation(impact_level)

def get_mission_impact(system_status, criticality):
    #Status / Mission Impact
    # X         | VL | L  | M  | H  | VH
    # Non Op    | L  | M  | H  | VH | VH
    # Major     | L  | M  | H  | H  | VH
    # Medium    | VL | L  | M  | H  | H
    # Minor     | VL | VL | L  | L  | M
    # Fully Op  | VL | VL | VL | VL | VL
    sys_index = system_status / 20

    return MISSION_IMPACT_DICT[sys_index][criticality]

def calculate_system_status(system, event_list=[]):
    # system dependency status
    # system dependency mission impact
    cyber_events = CyberEvent.objects.all().filter(is_resolved=False, system=system)
    system_status = get_system_status(system, cyber_events, event_list)
    system_dependencies = system.dependencies.all()
    if not system_dependencies:
        return system_status

    for s in system_dependencies:
        system_status = min(system_status, calculate_system_status(s, event_list))

    return system_status

def calculate_mission_impact(mission, criticality_dict={}, event_list=[]):
    mission_impact = 0
    for system in mission.systems.all():
        system_status = calculate_system_status(system, event_list)
        relationship = MissionToSystemAssociation.objects.all().filter(parent=mission, child=system)
        criticality = relationship[0].criticality if relationship else NONE
        criticality_dict[system.id] = criticality
        mission_impact = max(mission_impact, get_mission_impact(system_status, criticality))
        #print "system name: %s, status %s, criticality %s, mission impact %s"%(system.name, system_status, criticality, mission_impact)

    return mission_impact

def calculate_system_risk(system, threat_list=[]):
    sys_risk = system.risk if system.risk else 0
    vulnerabilities = Vulnerability.objects.all().filter(system=system)
    cve_list = [v.cve for v in vulnerabilities]
    threats = Threat.objects.all().filter(active=True, targeted_vulnerabilities__in=cve_list)

    threat_level = HIGH if threats else LOW

    vulnerability_level = VERY_LOW
    if threats:
        for threat in threats:
            for v in threat.targeted_vulnerabilities.all():
                if v in cve_list:
                    vulnerability_level = max(vulnerability_level, v.severity_score)
                    threat_list.append((threat, v, system))
    elif cve_list:
        for cve in cve_list:
            vulnerability_level = max(cve.severity_score)
            threat_list.append((None, cve, system))

    risk_level = LIKELIHOOD_RISK_DICT[threat_level][int(math.ceil(vulnerability_level/2))]
    risk_level = max(sys_risk, risk_level)

    return risk_level

def get_mission_risk(likelihood, impact):
    return MISSION_RISK_DICT[likelihood][impact]

#criticality_dict[system] = criticality ; relationship of system to mission
#threat_list (threat, CVE, system) ; used to build table of risks
def calculate_mission_risk(mission, criticality_dict={}, threat_list=[]):
    mission_risk = 0
    recalc_criticalities = False if criticality_dict else True
    for system in mission.systems.all():
        system_risk = calculate_system_risk(system, threat_list)
        if recalc_criticalities:
            relationship = MissionToSystemAssociation.objects.all().filter(parent=mission, child=system)
            criticality = relationship[0].criticality if relationship else NONE
            criticality_dict[system.id] = criticality
        else:
            criticality = criticality_dict[system.id]

        mission_risk = max(mission_risk, get_mission_risk(system_risk, criticality))
    return mission_risk
