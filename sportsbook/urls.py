from django.urls import path
from sportsbook import views

urlpatterns = [
    path('sportsbook/nba', views.sportsbook_nba, name='sportsbook-nba'),
    path('sportsbook/place-bet/<str:bet_id>', views.place_bet, name='sportsbook-place-bet'),
    path('sportsbook/my-bets', views.my_bets, name='sportsbook-my-bets'),
]
