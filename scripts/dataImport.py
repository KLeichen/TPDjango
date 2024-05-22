import csv

from stats.models import teamData, clubName



def run():
    with open('stats.csv') as file:
        reader = csv.reader(file)
        next(reader)

        clubName.objects.all().delete()
        teamData.objects.all().delete()

        for row in reader:

            club_name, _ = clubName.objects.get_or_create(name=row[0])

            team_data = teamData(
                        wins=row[1],
                        losses=row[2],
                        goals=row[3],
                        teamName=club_name)
            team_data.save()