from django.conf.urls import url

from . import views

app_name = 'mission_mapping'
urlpatterns = [
    # ex: /mission_mapping/
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^missions/$', views.missions, name='missions'),
    url(r'^systems/$', views.systems, name='systems'),
    url(r'^service_interruption/$', views.service_interruption, name='service_interruption'),
]
