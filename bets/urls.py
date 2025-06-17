from django.urls import path
from .views import (BetListView,
                    accept_bet,
                    bet_detail,
                    change_bet_status,
                    create_bet)


app_name = 'bets'

urlpatterns = [
    path('', BetListView.as_view(), name='list'),
    path('create/', create_bet, name='create_bet'),
    path('bet/<int:bet_id>/accept/', accept_bet, name='accept_bet'),
    path('bet/<int:bet_id>/', bet_detail, name='bet_detail'),
    path('bet/<int:bet_id>/change_status/',
         change_bet_status, name='change_status')
]
