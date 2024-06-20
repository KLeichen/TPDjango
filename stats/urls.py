from django.urls import path
from stats import views


urlpatterns = [
    path("", views.index, name="index"),
    path("table", views.table, name="table"),
    path("teams", views.teams, name="teams"),
    path("graph/<str:teamName>/<str:season>", views.graph, name="graph"),
    path("predict-winner/", views.predict_next_season_winner, name="predict_next_season_winner"),
    path("team-performance-ratios/<str:team_name>/", views.team_performance_ratios, name="team_performance_ratios"),
    path('team-list/', views.team_list, name='team_list'),
]
