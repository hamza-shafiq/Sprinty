# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from utils.clickup import ClickUp


def fetch_chart1(request, sprint_id):
    result = ClickUp().get_clickup_tasks(sprint_id=sprint_id)
    # project_details = ClickUp().get_projects_against_space(space_id=space_id)
    to_do = 0
    completed = 0
    for res in result:
        if res['status']['status'] == 'to do':
            to_do += 1
        else:
            completed += 1
    return {
        'donut_chart': {
            "todo": to_do,
            "completed": completed,
        }
    }


@login_required(login_url="/login/")
def index(request):
    html_template = loader.get_template('home/charts-morris.html')

    project_details = ClickUp().get_projects_against_space(space_id=3322943)
    sprint_id = project_details[0]['lists'][0]['id']
    context = fetch_chart1(request, sprint_id)
    context['donut_chart']['project'] = project_details
    context['segment'] = 'index'

    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
