from typing import Any
from django.db import models

# Create your models here.

class clubName(models.Model):
    name = models.CharField(max_length=255)
    # image_link = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class teamSeasonData(models.Model):
    wins = models.IntegerField()
    losses = models.IntegerField()
    goals = models.IntegerField()
    season = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    shots_att = models.IntegerField()
    on_target_att = models.IntegerField()
    woodwork = models.IntegerField()
    teamName = models.ForeignKey(clubName, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(self.name) + ',' + str(self.wins) + ',' + str(self.losses) + ',' + str(self.goals) + ',' + str(self.season) +\
                ',' + str(self.shots_att) + ',' + str(self.on_target_att) + ',' + str(self.woodwork) + ',' + str(self.teamName)
    

class ExtraSeasonData(models.Model):
    yel_cards = models.IntegerField()
    red_cards = models.IntegerField()
    header_goals = models.IntegerField()
    penalty_goals = models.IntegerField()
    freekick_goals = models.IntegerField()
    ibox_goals = models.IntegerField()
    obox_goals = models.IntegerField()
    fastbreak_goals = models.IntegerField()
    offsides = models.IntegerField()
    zero_goals = models.IntegerField()
    conceded_goals = models.IntegerField()
    saves = models.IntegerField()
    blocks = models.IntegerField()
    interceptions = models.IntegerField()
    tackles = models.IntegerField()
    last_man_tackles = models.IntegerField()
    clearances = models.IntegerField()
    own_goals = models.IntegerField()
    penalties_conceded = models.IntegerField()
    goals_from_penalties = models.IntegerField()
    passes = models.IntegerField()
    long_balls = models.IntegerField()
    crosses = models.IntegerField()
    corners = models.IntegerField()
    touches = models.IntegerField()
    penalties_saved = models.IntegerField()
    teamName = models.ForeignKey(clubName, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return "Name: " + str(self.teamName) +  \
            "Yellow Cards: " + str(self.yel_cards) + " Red Cards: " + str(self.red_cards) \
            + " Shots Att: " + str(self.shots_att) + " On Target Att: " + str(self.on_target_att) + \
            " Woodwork: " + str(self.woodwork) + " Header Goals: " + str(self.header_goals) + " Penalty Goals: " \
            + str(self.penalty_goals) + " Freekick Goals: " + str(self.freekick_goals) + " Ibox Goals: " + str(self.ibox_goals) \
            + " Obox Goals: " + str(self.obox_goals) + " Fastbreak Goals: " + str(self.fastbreak_goals) + " Offsides: " + str(self.offsides)\
            + " Zero Goals: " + str(self.zero_goals) + " Conceded Goals: " + str(self.conceded_goals) + " Saves: " + str(self.saves) \
            + " Blocks: " + str(self.blocks) + " Interceptions: " + str(self.interceptions) + " Tackles: " + str(self.tackles) \
            + " Last Man Tackles: " + str(self.last_man_tackles) + " Clearances: " + str(self.clearances) + " Own Goals: " + str(self.own_goals) \
            + " Penalties Conceded: " + str(self.penalties_conceded) + " Goals From Penalties: " + str(self.goals_from_penalties) \
            + " Passes: " + str(self.passes) + " Long Balls: " + str(self.long_balls) + " Crosses: " + str(self.crosses) \
            + " Corners: " + str(self.corners) + " Touches: " + str(self.touches) + " Penalties Saved: " + str(self.penalties_saved)
    

class ImageLinks(models.Model):
    image_link = models.CharField(max_length=255)
    club = models.ForeignKey(clubName, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(self.club)

