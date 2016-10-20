from django.shortcuts import render

# Create your views here.

def dashboard(request):
    context = {}
    return render(request, "index.html", context)

def missions(request):
    context = {}
    return render(request, "missions.html", context)

def add_mission(request):
    context = {}
    return render(request, "missions.html", context)

def systems(request):
    context = {}
    return render(request, "systems.html", context)

def service_interruption(request):
    context = {}
    return render(request, "service_interruption.html", context)
