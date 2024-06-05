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
    unique_names = list(team.values_list('name', flat=True).distinct())
    context = {
        "team": team,
        "img_link": img_link,
        "teamName": teamName,
        'unique_names': unique_names
    }
    return render(request,'teams.html', context)


def table(request):
    name = clubName.objects.all()
    season = teamSeasonData.objects.all()
    wins = season
    losses = season
    team = season
    teamName = season
    unique_seasons = list(season.values_list('season', flat=True).distinct())
    
    context = {
        "club": name,
        "wins": wins,
        "team": team,
        "teamName": teamName,
        "losses": losses,
        'season': season,
        'unique_season': unique_seasons
    }
    return render(request,'table.html', context)


def graph(request, teamName, season):
    plt.switch_backend('Agg') 
    id = 0
    inX = []
    inY = []
    woodX = []
    woodY = []
    outX = []
    outY = []
    team = teamSeasonData.objects.all()
    name = list(team.values_list('name', flat=True).distinct())
    for i in range(len(name)):
        if name[i] == teamName:
            id = i + 1
            break
    shots = list(teamSeasonData.objects.values_list().filter(season=season, teamName=id))
    for i in shots:
        shots_att = i[6]
        woodwork = i[7]
        on_target = i[8]
        shots_att = shots_att - on_target - woodwork
    for i in range(on_target):
        inX.append(random.randint(130,475))
        inY.append(random.randint(100,230))
    for i in range(woodwork):
        y = random.randint(75,275)
        a = random.randint(99,101)
        a *= random.choice([1,5])
        if y < 125 and y > 75:
            woodX.append(random.randint(99,505))
            woodY.append(75)
        else:
            woodX.append(a)
            woodY.append(y)
    for i in range(shots_att):
        y = random.randint(0,250)
        a = random.randint(0,580)
        if a < 510 and a > 90:
            outX.append(a)
            outY.append(random.randint(0, 65))
        else:
            outX.append(a)
            outY.append(y)
    im = plt.imread('/Users/kevo/HTML/Git Repo/TPDjango/stats/templates/SoccerGoal.jpeg')
    implot = plt.imshow(im)
    plt.scatter(inX, inY, marker='x', color='red', label='Goals')
    plt.scatter(woodX, woodY, marker='o', color='black', label='Woodwork')
    plt.scatter(outX, outY, label='Missed')
    plt.legend()
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)

    context = {
        "shots_att": shots_att,
        "woodwork": woodwork,
        "on_target": on_target,
        "team": team,
        "name": name,
        "teamName": teamName,
        "season": season,
        "id": id,
        "teamName": teamName,
        'data' : uri
    }
    return render(request,'graph.html', context)