
from django.urls import path

from apps.clickup import views
from apps.clickup.views import ReportsClass, no_of_sprints , tasks_against_sprint
app_name = "clickup"
urlpatterns = [
    path("", ReportsClass.as_view(), name='reports'),
    path("/sprints/", no_of_sprints, name='sprints'),
    path("/eachsprint/", tasks_against_sprint, name='sprints'),
]