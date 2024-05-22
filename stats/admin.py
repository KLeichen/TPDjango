from django.contrib import admin

from stats.models import teamData, clubName

# Register your models here.
admin.site.register(clubName)
admin.site.register(teamData)