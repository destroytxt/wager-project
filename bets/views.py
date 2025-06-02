from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import BetForm, UserForm
from .models import Bet


@login_required
def create_bet(request):
    if request.method == 'POST':
        form = BetForm(request.POST)
        if form.is_valid():
            bet = form.save(commit=False)
            bet.creator = request.user
            bet.save()
            return redirect('bets:list')
    else:
        form = BetForm()
    return render(request, 'bets/create_bet.html', {'form': form})


def bet_list(request):
    bets = Bet.objects.all()
    return render(request, 'bets/bet_list.html', {'bets': bets})


@login_required
def profile_view(request):
    user = request.user
    user_bets = (Bet.objects.filter(creator=user)
                 | Bet.objects.filter(opponent=user))

    if request.method == 'POST':
        form = BetForm(request.POST)
        if form.is_valid():
            bet = form.save(commit=False)
            bet.creator = user
            bet.save()
            return redirect('profile')
    else:
        form = BetForm()

    context = {
        'user': user,
        'bets': user_bets,
        'form': form,
    }
    return render(request, 'user/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserForm(instance=request.user)
    return render(request, 'user/edit_profile.html', {'form': form})
