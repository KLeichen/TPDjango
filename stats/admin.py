from django.contrib import admin

from stats.models import ExtraSeasonData, ImageLinks, teamSeasonData, clubName

# Register your models here.
admin.site.register(clubName)
admin.site.register(teamSeasonData)
admin.site.register(ExtraSeasonData)
admin.site.register(ImageLinks)