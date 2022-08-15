import json

import pytz
from django.shortcuts import render
from .models import Game, Bet
from django.forms.models import model_to_dict


def sportsbook_nba(request):

    games = Game.objects.all()

    game_dict = {}
    for game in games:
        game_dict[game.id] = model_to_dict(Game.objects.get(id=game.id))
        game_dict[game.id]['commence_time'] = game.commence_time.astimezone(pytz.timezone('US/Eastern'))\
            .strftime('%Y-%m-%d %H:%M:%S')
        game.commence_time = game.commence_time.astimezone(pytz.timezone('US/Eastern')).strftime('%m/%d/%Y, %I:%M %p')

    games_json = json.dumps(game_dict, default=str)
    context = {
        'games': games,
        'games_json': games_json
    }

    return render(request, 'sportsbook/nba.html', context)


def place_bet(request, bet_id):
    game_id = bet_id.split('_')[0]
    bet_team_code = bet_id.split('_')[1]
    bet_type_code = bet_id.split('_')[2]
    game = Game.objects.get(id=game_id)

    odds = ""
    spread = ""
    bet_team = ""
    bet_type = ""
    # spread bets
    if bet_type_code == 'spread' and bet_team_code == 'home':
        odds = game.home_team_odds
        spread = game.home_team_spread
        bet_team = game.home_team + ' ' + spread
        bet_type = 'SPREAD'
    elif bet_type_code == 'spread' and bet_team_code == 'away':
        odds = game.away_team_odds
        spread = game.away_team_spread
        bet_team = game.away_team + ' ' + spread
        bet_type = 'SPREAD'
    # moneyline bets
    elif bet_type_code == 'ml' and bet_team_code == 'home':
        odds = game.home_team_ml
        bet_team = game.home_team
        bet_type = 'MONEYLINE'
    elif bet_type_code == 'ml' and bet_team_code == 'away':
        odds = game.away_team_ml
        bet_team = game.away_team
        bet_type = 'MONEYLINE'
    # total bets
    elif bet_type_code == 'total' and bet_team_code == 'over':
        odds = "-110"
        bet_team = "Over 100"
        bet_type = 'TOTAL'
    elif bet_type_code == 'total' and bet_team_code == 'under':
        odds = "+110"
        bet_team = "Under 100"
        bet_type = 'TOTAL'

    if float(odds) > 0:
        odds_multiplier = (float(odds) / 100)
    else:
        odds_multiplier = (-100 / float(odds))

    if request.method == 'POST':
        try:
            bet_value = float(request.POST['bet-input'])
            bet_payout = bet_value * odds_multiplier

            new_bet = Bet.objects.create()
            new_bet.user = request.user
            new_bet.game = game
            new_bet.bet_type = bet_type
            new_bet.bet_team = bet_team_code
            new_bet.bet_team_name = bet_team
            new_bet.bet_odds = odds
            new_bet.bet_value = bet_value
            new_bet.bet_payout = bet_payout
            new_bet.save()

            request.user.profile.balance -= bet_value
            request.user.profile.save()

        except KeyError:
            print("Invalid Bet Amount")

    context = {
        'game': game,
        'bet_team': bet_team,
        'bet_type': bet_type,
        'odds': odds,
        'odds_multiplier': odds_multiplier
    }
    return render(request, 'sportsbook/place_bet.html', context)


def my_bets(request):

    bets = Bet.objects.filter(user=request.user).order_by('game__commence_time')

    context = {
        'bets': bets
    }
    return render(request, 'sportsbook/my_bets.html', context)
