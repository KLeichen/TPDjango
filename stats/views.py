from django_tables2.config import RequestConfig
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
from django.db.models import Sum, Max
from .tables import TeamTable
from .filters import TeamFilter
import django_tables2 as tables
from django.core.paginator import Paginator



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
        team_with_spaces = team  # Keep the team name with spaces
        if team_key in logos:
            merged_dict[team_key] = {'stats': stats, 'image_link': logos[team_key], 'name_with_spaces': team_with_spaces}
        else:
            merged_dict[team_key] = {'stats': stats, 'image_link': None, 'name_with_spaces': team_with_spaces}

    # Add remaining entries from logos
    for team, image_link in logos.items():
        team_key = team.replace(" ", "")  # Remove spaces from team name
        team_with_spaces = team  # Keep the team name with spaces
        if team_key not in merged_dict:
            merged_dict[team_key] = {'stats': None, 'image_link': image_link, 'name_with_spaces': team_with_spaces}

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
    return render(request, 'teams.html', context)

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
        'goals': goals,
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

    if season == None:
        shots = list(teamSeasonData.objects.filter(name=teamName).values_list())
    else:
        shots = list(teamSeasonData.objects.filter(season=season, name=teamName).values_list())

    total_shots_att = 0
    total_woodwork = 0
    total_on_target = 0

    for i in shots:
        total_shots_att += i[6]
        total_woodwork += i[7]
        total_on_target += i[8]
    

    shots_att = total_shots_att - total_on_target - total_woodwork

    for i in range(total_on_target):
        inX.append(random.randint(130,475))
        inY.append(random.randint(100,230))
    for i in range(total_woodwork):
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
        "woodwork": total_woodwork,
        "on_target": total_on_target,
        "team": team,
        "name": name,
        "teamName": teamName,
        "season": season,
        "id": id,
        "teamName": teamName,
        'data' : uri
    }
    return uri


def predict_next_season_winner(request):
    if request.method == 'POST':
        selected_season = request.POST.get('season')
        season_parts = selected_season.split('-')
        next_season = f"{int(season_parts[0]) + 1}-{int(season_parts[1]) + 1}"

        # Find the team with the most wins and least losses in the selected season
        best_team_selected_season = teamSeasonData.objects.filter(season=selected_season).order_by('-wins', 'losses').first()

        # Assuming the team with the most wins and least losses in the selected season could be the winner of the next season
        predicted_winner = best_team_selected_season.name if best_team_selected_season else None

        context = {
            'predicted_winner': predicted_winner,
            'selected_season': selected_season,
            'next_season': next_season,
            'team_performance': f"Wins: {best_team_selected_season.wins} Losses: {best_team_selected_season.losses}" if best_team_selected_season else "No data available"
        }
        return render(request, 'predict_winner.html', context)
    else:
        # Get all available seasons to populate the dropdown
        seasons = teamSeasonData.objects.values_list('season', flat=True).distinct()
        seasons = sorted(seasons)
        context = {
            'seasons': seasons
        }
        return render(request, 'select_season.html', context)


def team_performance_ratios(request, team_name):
    season = request.GET.get('season', None)

    if season:
        team_data = teamSeasonData.objects.filter(name=team_name, season=season)
    else:
        team_data = teamSeasonData.objects.filter(name=team_name)

    total_wins = team_data.aggregate(Sum('wins'))['wins__sum'] or 0
    total_losses = team_data.aggregate(Sum('losses'))['losses__sum'] or 0
    total_goals = team_data.aggregate(Sum('goals'))['goals__sum'] or 0

    win_loss_ratio = total_wins / total_losses if total_losses else float('inf')
    goals_to_wins_ratio = total_goals / total_wins if total_wins else 0

    # Calculate averages
    num_seasons = team_data.values('season').distinct().count()
    average_wins = total_wins / num_seasons if num_seasons else 0
    average_losses = total_losses / num_seasons if num_seasons else 0
    average_goals = total_goals / num_seasons if num_seasons else 0

    # Calculate position
    if season:
        teams_in_season = list(teamSeasonData.objects.filter(season=season).order_by('-wins', 'losses').values_list('name', flat=True).distinct())
        position = teams_in_season.index(team_name) + 1
    else:
        all_positions = []
        seasons = team_data.values_list('season', flat=True).distinct()
        for s in seasons:
            teams_in_season = list(teamSeasonData.objects.filter(season=s).order_by('-wins', 'losses').values_list('name', flat=True).distinct())
            pos = teams_in_season.index(team_name) + 1
            all_positions.append(pos)
        position = min(all_positions) if all_positions else None

    if season == None:
        shots = list(teamSeasonData.objects.filter(name=team_name).values_list())
    else:
        shots = list(teamSeasonData.objects.filter(season=season, name=team_name).values_list())

    total_shots_att = 0
    total_woodwork = 0
    total_on_target = 0

    for i in shots:
        total_shots_att += i[6]
        total_woodwork += i[7]
        total_on_target += i[8]
    
    shots_att = total_shots_att - total_on_target - total_woodwork

    context = {
        'team_name': team_name,
        'season': season if season else 'All Seasons',
        'win_loss_ratio': round(win_loss_ratio, 2),
        'goals_to_wins_ratio': round(goals_to_wins_ratio, 2),
        'average_wins': average_wins,
        'average_losses': average_losses,
        'average_goals': average_goals,
        'seasons': teamSeasonData.objects.filter(name=team_name).values_list('season', flat=True).distinct(),
        'shots_att': shots_att,
        'woodwork': total_woodwork,
        'on_target': total_on_target,
        'goals_per_match': round(total_goals / (total_wins + total_losses), 2) if (total_wins + total_losses) else 0,
        'position': position,
        'data': graph(request, team_name, season)
    }
    return render(request, 'team_performance_ratios.html', context)

def team_list(request):
    data = teamSeasonData.objects.all()
    filter = TeamFilter(request.GET, queryset=data)
    table = TeamTable(filter.qs)
    
    # Configure the table to be sortable and paginated
    RequestConfig(request, paginate={'per_page': 15}).configure(table)
    
    return render(request, 'team_list.html', {
        'table': table,
        'filter': filter,
    })


