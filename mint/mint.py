import sys
import os
import django

sys.path.append(os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arbet.settings")

django.setup()
from sportsbook.models import Game, Bet
from mint.models import Token


def generate_tokens(game):
    bets = Bet.objects.filter(game=game, bet_status='WIN')
    for bet in bets:
        if bet.bet_type == 'MONEYLINE':
            art = game.ml_win_art
        elif bet.bet_type == 'SPREAD':
            art = game.spread_win_art

        token = Token()
        token.bet = bet
        token.balance = bet.bet_value + bet.bet_payout
        token.mint_status = 'PENDING'
        token.art = art
        token.save()
