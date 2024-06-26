import django_tables2 as tables
from .models import teamSeasonData

class TeamTable(tables.Table):
    name = tables.Column(verbose_name='Team', accessor='name')

    def render_name(self, value, record):
        return f'{value}'

    class Meta:
        model = teamSeasonData
        template_name = 'django_tables2/bootstrap5.html'
        fields = ('name', 'wins', 'losses', 'goals', 'season')
        attrs = {"class": "django-tables2-table"}
