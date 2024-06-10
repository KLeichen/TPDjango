import base64
from collections import defaultdict
import io
import urllib
from django.http import HttpResponse
from django.shortcuts import render
import matplotlib
import urllib3
from stats.models import clubName, teamSeasonData, ExtraSeasonData, ImageLinks
import matplotlib.pyplot as plt
import random
from django.db.models import Sum


# Create your views here.
def index(request):
    return render(request, 'home.html')



def teams(request):
    teamName = teamSeasonData.objects.all()
    images = ImageLinks.objects.select_related('club').all()
    logos = {image.club.name.replace(" ", ""): image.image_link for image in images}
    team_stats = teamSeasonData.objects.values('name', 'season').annotate(
    total_goals=Sum('goals'),
    total_wins=Sum('wins'),
    total_losses=Sum('losses')
)

    # Create a dictionary with each team's name and its statistics for each season
    team_season_stats = defaultdict(lambda: {'goals': 0, 'wins': 0, 'losses': 0})
    team_total_stats = defaultdict(lambda: {'goals': 0, 'wins': 0, 'losses': 0})

    for entry in team_stats:
        team_name = entry['name']
        season_goals = entry['total_goals']
        season_wins = entry['total_wins']
        season_losses = entry['total_losses']
        team_season_stats[team_name][entry['season']] = {
            'goals': season_goals,
            'wins': season_wins,
            'losses': season_losses
    }
        team_total_stats[team_name]['goals'] += season_goals
        team_total_stats[team_name]['wins'] += season_wins
        team_total_stats[team_name]['losses'] += season_losses
    team_total_stats_all_seasons = dict(team_total_stats)
    merged_dict = {}

    for team, stats in team_total_stats_all_seasons.items():
        team_key = team.replace(" ", "")  # Remove spaces from team name
        if team_key in logos:
            merged_dict[team_key] = {'stats': stats, 'image_link': logos[team_key]}
        else:
            merged_dict[team_key] = {'stats': stats, 'image_link': None}

# Add remaining entries from test
    for team, image_link in logos.items():
        team_key = team.replace(" ", "")  # Remove spaces from team name
        if team_key not in merged_dict:
            merged_dict[team_key] = {'stats': None, 'image_link': image_link}
    goals = list(teamSeasonData.objects.values_list('goals', flat=True))
    team = clubName.objects.all()
    img_link = list(ImageLinks.objects.values_list())
    unique_names = list(team.values_list('name', flat=True).distinct())
    names_no_spaces = [name.replace(" ", "") for name in unique_names]
    team = list(clubName.objects.all())
    context = {
        "team": team,
        "url": img_link,
        "teamName": teamName,
        'unique_names': names_no_spaces,
        'goals': goals,
        'logos': logos,
        'test': merged_dict,
        }
    return render(request,'teams.html', context)
def table(request):
    name = clubName.objects.all()
    season = teamSeasonData.objects.all()
    wins = season
    losses = season
    team = season
    teamName = season
    goals = season
    unique_seasons = list(season.values_list('season', flat=True).distinct())
    
    context = {
        "club": name,
        "wins": wins,
        "team": team,
        "teamName": teamName,
        "losses": losses,
        'season': season,
        'unique_season': unique_seasons,
        'goals': goals
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
    im = plt.imread('stats/templates/SoccerGoal.jpeg')
    implot = plt.imshow(im)
    plt.scatter(inX, inY, marker='x', color='red', label='Goals')
    plt.scatter(woodX, woodY, marker='o', color='black', label='Woodwork')
    plt.scatter(outX, outY, label='Missed')
    plt.legend()
    plt.axis('off')
    plt.rcParams["figure.figsize"] = [9.00, 4.50]
    plt.rcParams["figure.autolayout"] = True
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf,format='png' , bbox_inches='tight', pad_inches=0.0)
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
