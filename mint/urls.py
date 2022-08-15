from django.urls import path

from mint import views

urlpatterns = [
    path('transfer', views.index, name='mint-index'),
    path('server-side-mint/', views.server_side_mint, name='server-side-mint'),
    path('deposit', views.deposit, name='deposit'),
    path('mint/token/<str:token_id>', views.view_token, name='mint-view-token'),
]
