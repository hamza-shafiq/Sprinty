from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
# from django.template import loader
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from utils.clickup import ClickUp


def get_donut_chart(sprint_id):
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


def no_of_sprints(request):
    project_id = request.GET.get("value")
    selected_proj_sprint_list = ClickUp().get_sprints_against_project(project_id)
    report1 = {"todo": 0, "completed": 0}

    for row in selected_proj_sprint_list:
        result = ClickUp().get_clickup_tasks(sprint_id=row['id'])
        for res in result:
            if res['status']['status'] == 'to do':
                report1['todo'] += 1
            else:
                report1['completed'] += 1
#team velocity
    sprints = ClickUp().get_sprints_against_project(project_id=project_id)
    sprint_wise_velocity = []
    for row in sprints:
        if row["name"].startswith('Sprint'):
            result = ClickUp().get_team_velocity(sprint_id=row['id'])
            time_estimate = [x.get('time_estimate') for x in result]
            time_estimates = round(((sum(list(filter(None, time_estimate)))) / 3600000), 2)
            time_tracked = round(((sum([x.get('time_spent', 0) for x in result])) / 3600000), 2)

            sprint_wise_velocity.append({
                "y": str(row["name"]).split("(")[0],
                "a": time_estimates,
                "b": time_tracked,
            })

    return JsonResponse({
        "sprints": selected_proj_sprint_list,
        "donut_chart": report1,
        "team_velocity": sprint_wise_velocity,
    }, status=200)


def tasks_against_sprint(request):
    project_id = request.GET.get("value")
    sprint_id = request.GET.get("sprint")
    result = ClickUp().get_clickup_tasks(sprint_id=sprint_id)
    report1 = {"todo": 0, "completed": 0}
    for res in result:
        if res['status']['status'] == 'to do':
            report1['todo'] += 1
        else:
            report1['completed'] += 1
    return JsonResponse({
        "donut_chart": report1}, status=200)


def team_velocity(request):
    project_id = request.GET.get("value")
    sprints = ClickUp().get_sprints_against_project(project_id=project_id)
    sprint_wise_velocity = []
    for row in sprints:
        if row["name"].startswith('Sprint'):
            result = ClickUp().get_team_velocity(sprint_id=row['id'])
            time_estimate = [x.get('time_estimate') for x in result]
            time_estimates = round(((sum(list(filter(None, time_estimate)))) / 3600000), 2)
            time_tracked = round(((sum([x.get('time_spent', 0) for x in result])) / 3600000), 2)

            sprint_wise_velocity.append({
                "y": str(row["name"]).split("(")[0],
                "a": time_estimates,
                "b": time_tracked,
            })

    return JsonResponse({"team_velocity": sprint_wise_velocity}, status=200)


def average_team_velocity(request):
    project_id = request.GET.get("value")
    sprints = ClickUp().get_sprints_against_project(project_id=97386452)
    no_of_sprints = len(sprints)
    t_hours = 0
    for row in sprints:
        result = ClickUp().get_team_velocity(sprint_id=row['id'])
        time_tracked = [x.get('time_spent', 0) for x in result]
        time_tracked = sum(time_tracked)
        t_hour = (time_tracked / 3600000)
        t_hours += t_hour
    average_velocity = t_hours/no_of_sprints

    return JsonResponse({
        "Average_velocity": average_velocity,
    }, status=200)







