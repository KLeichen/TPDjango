import base64
import io
import urllib
from django.http import HttpResponse
from django.shortcuts import render
import matplotlib
import urllib3
from stats.models import clubName, teamSeasonData, ExtraSeasonData, ImageLinks
import matplotlib.pyplot as plt
import random

# Create your views here.
def index(request):
    return render(request, 'home.html')



def teams(request):
    teamName = teamSeasonData.objects.all()
    team = clubName.objects.all()
    img_link = ImageLinks.objects.all()
    context = {
        "team": team,
        "img_link": img_link,
        "teamName": teamName
    }
    return render(request,'teams.html', context)


def table(request):
    name = clubName.objects.all()
    wins = teamSeasonData.objects.all()
    team = teamSeasonData.objects.all()
    teamName = teamSeasonData.objects.all()
    losses = teamSeasonData.objects.all()
    season = teamSeasonData.objects.all()
    unique_seasons = season.values_list('season', flat=True).distinct()
    
    context = {
        "club": name,
        "wins": wins,
        "team": team,
        "teamName": teamName,
        "losses": losses,
        'season': season,
        'unique_season': list(unique_seasons)
    }
    return render(request,'table.html', context)