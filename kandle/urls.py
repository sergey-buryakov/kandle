"""kandle URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import re_path
from django.conf.urls import include
from kandleapp import views
#============================
from social_django.urls import extra

urlpatterns = [
    re_path(r'^$', views.index),
    re_path(r'^sign_up$', views.sign_up),
    re_path(r'^dashboard$', views.userdash),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    re_path(r'^create', views.create),
    re_path(r'^event/(?P<eventid>.+)', views.event), #add regex
    re_path(r'^oauth/complete/(?P<backend>[^/]+){0}$'.format(extra), views.complete, name='complete'),
    re_path(r'^oauth/', include('social_django.urls', namespace='social')),
    re_path(r'^settings/$', views.settings, name='settings'),
    re_path(r'^settings/password/$', views.password, name='password'),
]