from typing import Any
from django.db import models

# Create your models here.

class clubName(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class teamData(models.Model):
    wins = models.CharField(max_length=255)
    losses = models.CharField(max_length=255)
    goals = models.CharField(max_length=255)
    teamName = models.ForeignKey(clubName, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return "Wins: " + str(self.wins) + " losses: " + str(self.losses) + " goals: " + str(self.goals)
    
