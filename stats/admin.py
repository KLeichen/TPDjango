from django.contrib import admin

from stats.models import ExtraData, teamData, clubName

# Register your models here.
admin.site.register(clubName)
admin.site.register(teamData)
admin.site.register(ExtraData)
# admin.site.register(Season)