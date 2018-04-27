#-*- coding:utf-8 -*-
from django.conf.urls import patterns, url
from Cdatos import views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = patterns('',
                       url(r'^$', views.gis, name="gis"),
                      )

urlpatterns += staticfiles_urlpatterns()
