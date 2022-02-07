from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template import loader
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from utils.clickup import ClickUp


@method_decorator(login_required(login_url='/login'), name="dispatch")
class ReportsClass(TemplateView):
    template_name = 'home/charts-morris.html'

    def get(self, request, *args, **kwargs):
        result = ClickUp().get_clickup_tasks(sprint_id=169390750)
        project_details = ClickUp().get_projects_against_space(space_id=55430882)

        to_do = 0
        completed = 0
        for res in result:
            if res['status']['status'] == 'to do':
                to_do += 1
            else:
                completed += 1
        context = {
            'donut_chart': {
                "todo": to_do,
                "completed": completed,
                "project": project_details,
            }
        }
        return render(request, self.template_name, context=context)


def no_of_sprints(request):
    project_id = request.GET.get("value")
    sprints = ClickUp().get_sprints_against_project(project_id)
    return JsonResponse({"sprints": sprints}, status=200)



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
