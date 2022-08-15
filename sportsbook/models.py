from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.


class Game(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    sport_key = models.CharField(max_length=20)
    commence_time = models.DateTimeField()
    last_update = models.DateTimeField(default=now)
    home_team = models.CharField(max_length=100)
    home_team_odds = models.CharField(max_length=20)
    home_team_spread = models.CharField(max_length=20)
    home_team_ml = models.CharField(max_length=20)
    away_team = models.CharField(max_length=100)
    away_team_odds = models.CharField(max_length=20)
    away_team_spread = models.CharField(max_length=20)
    away_team_ml = models.CharField(max_length=20)
    home_team_score = models.IntegerField(default=0)
    away_team_score = models.IntegerField(default=0)
    game_status = models.CharField(max_length=20, default='Not Started')
    ml_win_art = models.ImageField(upload_to='ml_win_art', blank=True)
    spread_win_art = models.ImageField(upload_to='spread_win_art', blank=True)

    def __str__(self):
        return self.home_team + " vs " + self.away_team + " at " + str(self.commence_time)


class Bet(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, null=True, blank=True, on_delete=models.CASCADE)
    bet_type = models.CharField(max_length=20)
    bet_team = models.CharField(max_length=20)
    bet_team_name = models.CharField(max_length=100)
    bet_odds = models.CharField(max_length=20)
    bet_value = models.FloatField(default=0.0)
    bet_payout = models.FloatField(default=0.0)
    bet_status = models.CharField(max_length=20)

    def __str__(self):
        return self.bet_team + " " + self.bet_type + " " + str(self.game)
