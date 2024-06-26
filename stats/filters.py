import django_filters
from .models import teamSeasonData

class TeamFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    season = django_filters.ChoiceFilter(choices=lambda: [(season, season) for season in teamSeasonData.objects.values_list('season', flat=True).distinct()])
    goals = django_filters.ChoiceFilter(choices=lambda: [(goal, goal) for goal in teamSeasonData.objects.values_list('goals', flat=True).distinct()])
    losses = django_filters.ChoiceFilter(choices=lambda: [(loss, loss) for loss in teamSeasonData.objects.values_list('losses', flat=True).distinct()])
    wins = django_filters.ChoiceFilter(choices=lambda: [(win, win) for win in teamSeasonData.objects.values_list('wins', flat=True).distinct()])

    class Meta:
        model = teamSeasonData
        fields = ['name', 'season', 'goals', 'losses', 'wins']
