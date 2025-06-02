from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BetForm, BetStatusForm, UserForm
from .models import Bet, User


@login_required
def create_bet(request):
    if request.method == 'POST':
        form = BetForm(request.POST)
        if form.is_valid():
            bet = form.save(commit=False)
            bet.creator = request.user
            if not bet.arbiter:
                bet.arbiter = User.objects.filter(is_superuser=True).first()
            bet.save()
            return redirect('bets:list')
    else:
        form = BetForm()
    return render(request, 'bets/create_bet.html', {'form': form})


@login_required
def change_bet_status(request, bet_id):
    bet = get_object_or_404(Bet, id=bet_id)
    if request.user != bet.arbiter:
        return render(request, '403.html', status=403)
    if request.method == 'POST':
        form = BetStatusForm(request.POST, instance=bet)
        if form.is_valid():
            form.save()
            return redirect('bets:bet_detail', bet.id)
    else:
        form = BetStatusForm(instance=bet)
    return render(request, 'bets/change_status.html',
                  {'form': form, 'bet': bet})


def bet_list(request):
    bets = Bet.objects.all()
    return render(request, 'bets/bet_list.html', {'bets': bets})


def bet_detail(request, bet_id):
    bet = get_object_or_404(Bet, id=bet_id)
    return render(request, 'bets/bet_detail.html', {'bet': bet})


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
