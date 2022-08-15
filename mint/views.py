from django.shortcuts import render, redirect
from .models import Token
from sportsbook.views import sportsbook_nba
import re
import requests

def home(request):
    return render(request, 'mint/home.html')


def index(request):
    return render(request, 'mint/index.html')


def server_side_mint(request):
    context = {

    }

    return render(request, 'mint/server_side_mint.html', context)


def deposit(request):

    MOBILE_AGENT_RE=re.compile(r".*(iphone|mobile|androidtouch)",re.IGNORECASE)

    if MOBILE_AGENT_RE.match(request.META['HTTP_USER_AGENT']):
        print(True)
    else:
        print(False)

    response = requests.get(
        'https://api.coinbase.com/v2/exchange-rates?currency=ETH')

    response = response.json()

    eth_to_usd = response['data']['rates']['USD']

    context = {
        "rate": eth_to_usd
    }

    if request.method == 'POST':
        try:
            deposit_value = float(request.POST['depositVal'])
            request.user.profile.balance += deposit_value / 1e+18
            request.user.profile.save()

            return redirect(sportsbook_nba)

        except KeyError:
            print("Invalid Deposit Amount")

    return render(request, 'mint/deposit.html', context)


def view_token(request, token_id):

    token = Token.objects.get(id=token_id)

    context = {
        "token": token
    }

    if request.method == 'POST' and 'liquidate' in request.POST:
        token.mint_status = 'LIQUIDATED'
        token.save()
        request.user.profile.balance += token.balance
        request.user.profile.save()

    if request.method == 'POST' and 'mint' in request.POST:
        print('minted')
        token.mint_status = 'MINTED'
        token.save()

    return render(request, 'mint/view_token.html', context)
