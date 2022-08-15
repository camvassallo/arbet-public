from datetime import datetime

import requests
import sys
import os
import django
import pytz

sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arbet.settings")

django.setup()
from sportsbook.models import Game

# Get all NBA games from the API
def get_nba_games():
    response = requests.get(
        'https://api.the-odds-api.com/v4/sports/basketball_nba/odds/?apiKey=c0d36a7f096d05f6e1d483c07f0f6754'
        '&regions=us&markets=h2h,spreads&oddsFormat=american')

    response = response.json()

    # # Opening JSON file
    # f = open('sportsbook/sample.json')
    #
    # # returns JSON object as
    # # a dictionary
    # response = json.load(f)

    for r in response:
        id = r['id']
        sport_key = r['sport_key']
        commence_time_str = r['commence_time']
        commence_time = datetime.strptime(commence_time_str, "%Y-%m-%dT%H:%M:%S%z")
        home_team = r['home_team']
        away_team = r['away_team']

        home_team_ml = 0
        away_team_ml = 0

        h2h_outcomes = r['bookmakers'][0]['markets'][0]['outcomes']
        for outcome in h2h_outcomes:
            if outcome['name'] == home_team:
                home_team_ml = outcome['price']
                if home_team_ml > 0:
                    home_team_ml = '+' + str(home_team_ml)
            else:
                away_team_ml = outcome['price']
                if away_team_ml > 0:
                    away_team_ml = '+' + str(away_team_ml)

        home_team_odds = 0
        home_team_spread = 0
        away_team_odds = 0
        away_team_spread = 0

        spread_outcomes = []

        try:
            spread_outcomes = r['bookmakers'][0]['markets'][1]['outcomes']
        except:
            pass
        if spread_outcomes:
            for outcome in spread_outcomes:
                if outcome['name'] == home_team:
                    home_team_odds = outcome['price']
                    home_team_spread = outcome['point']
                    if home_team_spread > 0:
                        home_team_spread = '+' + str(home_team_spread)
                else:
                    away_team_odds = outcome['price']
                    away_team_spread = outcome['point']
                    if away_team_spread > 0:
                        away_team_spread = '+' + str(away_team_spread)

        game = Game(id, sport_key, commence_time,
                    home_team, home_team_odds, home_team_spread, home_team_ml,
                    away_team, away_team_odds, away_team_spread, away_team_ml)

        game.save()


# Main function
get_nba_games()
