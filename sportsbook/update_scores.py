import json
from datetime import datetime

import sys
import os
import django

sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arbet.settings")

django.setup()
from sportsbook.models import Game, Bet
from mint.dalle import generate_art
from mint.mint import generate_tokens

now = datetime.now()
import pytz

utc = pytz.UTC


def update_bets(game):
    home_spread_win = False
    away_spread_win = False
    home_ml_win = False
    away_ml_win = False

    # TODO
    # over_win = False
    # under_win = False

    if game.home_team_score > game.away_team_score:
        home_ml_win = True
    if game.away_team_score > game.home_team_score:
        away_ml_win = True
    if game.home_team_score + float(game.home_team_spread) > game.away_team_score:
        home_spread_win = True
    if game.away_team_score + float(game.away_team_spread) > game.home_team_score:
        away_spread_win = True

    bets = Bet.objects.filter(game=game)

    for bet in bets:
        if bet.bet_type == 'MONEYLINE':
            if bet.bet_team == 'home':
                if home_ml_win:
                    bet.bet_status = 'WIN'
                elif away_ml_win:
                    bet.bet_status = 'LOSE'
                else:
                    bet.bet_status = 'PUSH'
            if bet.bet_team == 'away':
                if away_ml_win:
                    bet.bet_status = 'WIN'
                elif home_ml_win:
                    bet.bet_status = 'LOSE'
                else:
                    bet.bet_status = 'PUSH'
        elif bet.bet_type == 'SPREAD':
            if bet.bet_team == 'home':
                if home_spread_win:
                    bet.bet_status = 'WIN'
                elif away_spread_win:
                    bet.bet_status = 'LOSE'
                else:
                    bet.bet_status = 'PUSH'
            elif bet.bet_team == 'away':
                if away_spread_win:
                    bet.bet_status = 'WIN'
                elif home_spread_win:
                    bet.bet_status = 'LOSE'
                else:
                    bet.bet_status = 'PUSH'

        bet.save()

    return [home_ml_win, away_ml_win, home_spread_win, away_spread_win]


# Get all NBA games from the API
def get_nba_games():
    # response = requests.get(
    #     'https://api.the-odds-api.com/v4/sports/basketball_nba/scores/?apiKey=c0d36a7f096d05f6e1d483c07f0f6754'
    #     '&daysFrom=3')
    #
    # response = response.json()

    # Opening JSON file
    f = open('sportsbook/score_sample.json')

    # returns JSON object as
    # a dictionary
    response = json.load(f)

    for r in response:
        game_id = r['id']
        game = Game.objects.get(id=game_id)

        if game.game_status != 'Completed':
            game.last_update = r['last_update']
            commence_time_str = r['commence_time']
            game.commence_time = datetime.strptime(commence_time_str, "%Y-%m-%dT%H:%M:%S%z")

            if utc.localize(now) > game.commence_time:
                game.game_status = 'In Progress'
                game.home_team_score = 0
                game.away_team_score = 0
            else:
                game.game_status = "Not Started"

            if r.get('scores'):
                home_score = r['scores'][0]['score']
                away_score = r['scores'][1]['score']
                game.home_team_score = int(home_score)
                game.away_team_score = int(away_score)

            completed = r['completed']
            if completed:
                print(game.away_team + ' @ ' + game.home_team + ' completed. Generating artwork')
                game.game_status = 'Completed'
                outcomes = update_bets(game)
                if outcomes[0]:
                    generate_art(game, 'home_ml_win')
                if outcomes[1]:
                    generate_art(game, 'away_ml_win')
                if outcomes[2]:
                    generate_art(game, 'home_spread_win')
                if outcomes[3]:
                    generate_art(game, 'away_spread_win')

                generate_tokens(game)
            game.save()


# Main function
get_nba_games()
