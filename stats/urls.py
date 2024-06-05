from django.urls import path
from stats import views


urlpatterns = [
    path("", views.index, name="index"),
    path("table", views.table, name="table"),
    path("teams", views.teams, name="teams"),
    path("graph/<str:teamName>/<str:season>", views.graph, name="graph")
]
