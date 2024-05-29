from django.urls import path
from stats import views


urlpatterns = [
    path("", views.index, name="index"),
    path("<str:team_name>", views.graph, name="graph"),
]
