from django.conf.urls import url

from . import views

app_name = 'mission_mapping'
urlpatterns = [
    # ex: /mission_mapping/
    url(r'^$', views.missions, name='missions'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^missions/$', views.missions, name='missions'),
    url(r'^missions/(?P<mission_id>[0-9]+)/$', views.mission, name='mission'),
    url(r'^mission_types/$', views.mission_types, name='mission_types'),
    url(r'^services/$', views.systems, name='services'),
    url(r'^services/(?P<system_id>[0-9]+)/$', views.system, name='service'),
    url(r'^service_interruption/$', views.service_interruption, name='service_interruption'),
]
