import django_tables2 as tables
from .models import teamSeasonData

class TeamTable(tables.Table):
    name = tables.Column(verbose_name='Team', accessor='name')

    def render_name(self, value, record):
        url = f"/graph/{record.name}/{record.season}"
        return f'<a href="{url}">{value}</a>'

    class Meta:
        model = teamSeasonData
        template_name = 'django_tables2/bootstrap.html'
        fields = ('name', 'wins', 'losses', 'goals', 'season')
        per_page = 10  # Set the number of items per page here
