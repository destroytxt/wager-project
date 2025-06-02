from django.urls import path
from .views import bet_list, create_bet


app_name = 'bets'

urlpatterns = [
    path('', bet_list, name='list'),
    path('create/', create_bet, name='create_bet'),
]
