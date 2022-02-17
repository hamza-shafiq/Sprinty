# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.clickup.views import no_of_sprints, tasks_against_sprint
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path("sprints/", no_of_sprints, name='sprints'),
    path("eachsprint/", tasks_against_sprint, name='sprints'),

    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
