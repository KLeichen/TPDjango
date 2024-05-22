import base64
import io
import urllib
from django.http import HttpResponse
from django.shortcuts import render
import matplotlib
import urllib3
from stats.models import clubName, teamData
import matplotlib.pyplot as plt

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
    a = []
    b = []
    for i in teamData.objects.all():
        a.append(i.teamName.name)
        b.append(float(i.wins))
    plt.bar(a, b)
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf,format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)
    return render(request,'graph.html',{'data':uri})

    
