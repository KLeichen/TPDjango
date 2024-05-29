from django.contrib import admin

from stats.models import ExtraSeasonData, teamSeasonData, clubName

# Register your models here.
admin.site.register(clubName)
admin.site.register(teamSeasonData)
admin.site.register(ExtraSeasonData)
