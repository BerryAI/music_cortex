# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
import views as user_views



urlpatterns = [

    url(r'artists/$', 'apis.views.artists'),
    url(r'^albums/$', 'apis.views.albums'),
    url(r'^tracks/$', 'apis.views.tracks'),
    url(r'^countries/$', 'apis.views.countries'),
    url(r'^genres/$', 'apis.views.genres'),
    url(r'^decades/$', 'apis.views.decades'),
    url(r'^recommend/$', 'apis.views.recommend'),
    url(r'^feedback/$', 'apis.views.feedback'),
    

]    