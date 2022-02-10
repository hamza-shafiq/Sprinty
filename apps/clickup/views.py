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


@method_decorator(login_required(login_url='/login'), name="dispatch")
class ReportsClass(TemplateView):
    template_name = 'home/charts-morris.html'

    def get(self, request, *args, **kwargs):
        project_details = ClickUp().get_projects_against_space(space_id=55430882)
        sprint_id = project_details[0]['lists'][0]['id']
        context = fetch_chart1(request, sprint_id)
        context['donut_chart']['project'] = project_details
        return render(request, self.template_name, context=context)


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

    return JsonResponse({
        "sprints": selected_proj_sprint_list,
        "donut_chart": report1,
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

# def reports(request):
#     result = ClickUp().get_clickup_tasks(sprint_id=169390750)
#     todo = result['todo']
#     completed = result['completed']
#
#     context = {
#         'donut_chart': {
#             "todo": todo,
#             "completed": completed
#         }
#     }
#     html_template = loader.get_template('home/charts-morris.html')
#     return HttpResponse(html_template.render(context, request))
