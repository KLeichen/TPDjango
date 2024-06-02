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
    name = clubName.objects.all()
    wins = teamSeasonData.objects.all()
    team = teamSeasonData.objects.all()
    teamName = teamSeasonData.objects.all()
    losses = teamSeasonData.objects.all()
    season = teamSeasonData.objects.all()
    context = {
        "club": name,
        "wins": wins,
        "team": team,
        "teamName": teamName,
        "losses": losses,
        'season': season
    }
    return render(request, 'index.html', context)

def graph(request, team_name):
    # matplotlib.use('agg')
    # test_list = []
    # test_list2 = []
    # im = plt.imread('/Users/kevo/HTML/Git Repo/TPDjango/stats/templates/SoccerGoal.jpeg')
    # implot = plt.imshow(im)
    # plt.scatter(test_list, test_list2, marker='x', color='red')
    # plt.show
    # fig = plt.gcf()
    # buf = io.BytesIO()
    # fig.savefig(buf,format='png')
    # buf.seek(0)
    # string = base64.b64encode(buf.read())
    # uri =  urllib.parse.quote(string)
    # return render(request,'graph.html',{'data':uri})
    teamName = teamSeasonData.objects.all()
    team = clubName.objects.all()
    img_link = ImageLinks.objects.all()
    context = {
        "team": team,
        "img_link": img_link,
        "teamName": teamName
    }
    return render(request,'teams.html', context)