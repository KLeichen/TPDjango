import base64
import io
import urllib
from django.http import HttpResponse
from django.shortcuts import render
import matplotlib
import urllib3
from stats.models import clubName, teamData, ExtraData
import matplotlib.pyplot as plt
import random

# Create your views here.
def index(request):
    name = clubName.objects.all()
    wins = teamData.objects.all()
    team = teamData.objects.all()
    teamName = teamData.objects.all()
    losses = teamData.objects.all()
    context = {
        "club": name,
        "wins": wins,
        "team": team,
        "teamName": teamName,
        "losses": losses
    }
    return render(request, 'index.html', context)

def graph(request):
    matplotlib.use('agg')
    shots_att = ExtraData.objects.all()
    on_target_att = ExtraData.objects.all()
    woodwork = ExtraData.objects.all()
    count = 0
    test_list = []
    test_list2 = []
    for shots in shots_att:
        count += 1
    for i in range(count):
        test_list.append(random.randint(0,300))
        test_list2.append(random.randint(0,300))
    im = plt.imread('/Users/kevo/HTML/Git Repo/TPDjango/stats/templates/arco.jpeg')
    implot = plt.imshow(im)
    plt.scatter(test_list, test_list2)
    plt.show
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)
    return render(request,'graph.html',{'data':uri})