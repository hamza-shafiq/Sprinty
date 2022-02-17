import requests
# from django.http import HttpResponse
# from rest_framework import status
# from rest_framework.response import Response


class ClickUp:
    def __init__(self):
        self.base_url = "https://api.clickup.com/api/v2/"
        # self.token = "3523293_40190610fa6da3b679fc2914d54be43b75e8c9d5"
        self.token = "pk_3344634_YWC3QN6RWXQL9JMFG7UOV5UG3CC30TLB"
        self.header = {"Authorization": self.token}

    def get_clickup_space(self, space_id):
        url = self.base_url + "space/" + str(space_id)
        r = requests.get(url, headers=self.header)

        resp = {}
        if r.status_code == 200:
            data = r.json()
            resp = {"space_id": data["id"], "space_name": data["name"]}

        return resp

    def get_projects_against_space(self, space_id):
        url = self.base_url + "space/" + str(space_id) + "/folder"
        r = requests.get(url, headers=self.header)

        resp = {}
        if r.status_code == 200:
            data = r.json()
            resp = data['folders']
        return resp

    def get_sprints_against_project(self, project_id):
        url = self.base_url + "folder/" + str(project_id) + "/list"
        r = requests.get(url, headers=self.header)

        resp = {}
        if r.status_code == 200:
            data = r.json()
            resp = data['lists']
        return resp

    # def get_specific_sprint_against_project(self, sprint_id):
    #     url = self.base_url + "list/" + str(sprint_id)
    #     r = requests.get(url, headers=self.header)
    #
    #     if r.status_code == 200:
    #         data = r.json()
    #         resp = data['']

    def get_clickup_tasks(self, sprint_id):
        url = self.base_url + "list/" + str(sprint_id) + "/task?archived=false&status%5B%5D=complete&include_closed=true"
        r = requests.get(url, headers=self.header)
        resp = {}
        if r.status_code == 200:
            data = r.json()
            resp = data['tasks']

        return resp

    def get_team_velocity(self, sprint_id):
        url = self.base_url + "list/" + str(sprint_id) + "/task"
        r = requests.get(url, headers=self.header)
        resp = {}
        if r.status_code == 200:
            data = r.json()
            resp = data['tasks']

        return resp

    # def get_clickup_task(self, task_id):
    #     url = self.base_url + "task/" + str(task_id)
    #     r = requests.get(url, headers=self.header)
    #
    #     if r.status_code == 200:
    #         data = r.json()


# ClickUp().get_clickup_space(space_id=55430882)
# ClickUp().get_projects_against_space(space_id=55430882)
# ClickUp().get_sprints_against_project(project_id=103318183)
# ClickUp().get_clickup_list(list_id=169390750)
# ClickUp().get_clickup_tasks(sprint_id=169390750)
ClickUp().get_team_velocity(sprint_id=163340490)
# ClickUp().get_clickup_task(task_id='201rb33')
