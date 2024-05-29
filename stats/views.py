import base64
import io
import urllib
from django.http import HttpResponse
from django.shortcuts import render
import matplotlib
import urllib3
from stats.models import clubName, teamSeasonData, ExtraSeasonData
import matplotlib.pyplot as plt
import random

# Create your views here.
def index(request):
    name = clubName.objects.all()
    wins = teamSeasonData.objects.all()
    team = teamSeasonData.objects.all()
    teamName = teamSeasonData.objects.all()
    losses = teamSeasonData.objects.all()
    context = {
        "club": name,
        "wins": wins,
        "team": team,
        "teamName": teamName,
        "losses": losses
    }
    return render(request, 'index.html', context)

def graph(request, team_name):
    matplotlib.use('agg')
    shots_att = ExtraSeasonData.objects.get(on_target_att=100)
    # shots_att = ExtraSeasonData.objects.get(on_target_att=team_name)
    # on_target_att = ExtraSeasonData.objects.get(team_name)
    # woodwork = ExtraSeasonData.objects.get(team_name)
    count = 0
    test_list = []
    test_list2 = []
    for shots in shots_att:
        count += 1
    for i in range(count):
        test_list.append(random.randint(0, 500))
        test_list2.append(random.randint(100,250))
    im = plt.imread('/Users/kevo/HTML/Git Repo/TPDjango/stats/templates/SoccerGoal.jpeg')
    implot = plt.imshow(im)
    plt.scatter(test_list, test_list2, marker='x', color='red')
    plt.show
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)
    return render(request,'graph.html',{'data':uri})