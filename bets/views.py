import copy

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView

from .forms import AcceptBetForm, BetForm, BetStatusForm, UserForm
from .models import Bet, User


@login_required
def create_bet(request):
    if request.method == 'POST':
        form = BetForm(request.POST, user=request.user)
        if form.is_valid():
            bet = form.save(commit=False)
            bet.creator = request.user
            if not bet.arbiter:
                bet.arbiter = User.objects.filter(is_superuser=True).first()
            if not bet.arbiter:
                form.add_error(
                    'arbiter', 'Без арбитра невозможно заключить пари.')
            if bet.arbiter in (bet.creator, bet.opponent):
                form.add_error(
                    'arbiter', 'Арбитр не может быть участником пари.')
            elif bet.status == 'open' and request.user.balance < bet.amount:
                form.add_error(
                    'amount', 'Недостаточно средств для создания пари.')
            else:
                if bet.status == 'open':
                    request.user.balance -= bet.amount
                    request.user.save()
                bet.save()
                return redirect('bets:list')
    else:
        form = BetForm(user=request.user)
    return render(request, 'bets/create_bet.html', {'form': form})


@login_required
def accept_bet(request, bet_id):
    bet = get_object_or_404(Bet, id=bet_id)
    form = AcceptBetForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            if bet.status != 'open':
                form.add_error(None, 'Пари уже не активно.')
            elif bet.opponent_accepted:
                form.add_error(None, 'Вы уже приняли участие.')
            elif request.user.balance < bet.amount:
                form.add_error(None, 'Недостаточно средств на счёте.')
            else:
                request.user.balance -= bet.amount
                request.user.save()
                bet.opponent_accepted = True
                bet.status = 'accepted'
                bet.opponent = request.user
                bet.save()
                return redirect('bets:bet_detail', bet.id)
    return render(request, 'bets/accept_bet.html', {'form': form, 'bet': bet})


@login_required
def change_bet_status(request, bet_id):
    bet = get_object_or_404(Bet, id=bet_id)
    if request.user != bet.arbiter:
        return render(request, 'pages/403.html', status=403)
    if request.method == 'POST':
        form = BetStatusForm(request.POST, instance=copy.copy(bet))
        if form.is_valid():
            cleaned = form.cleaned_data
            bet.status = cleaned['status']
            bet.winner = cleaned.get('winner')
            if bet.status == 'finished' and not bet.opponent:
                bet.winner.balance += bet.amount
                bet.winner.save()
            elif bet.status == 'finished' and bet.winner and bet.opponent:
                total_amount = bet.amount * 2
                bet.winner.balance += total_amount
                bet.winner.save()
            elif bet.status == 'cancelled':
                if bet.creator:
                    bet.creator.balance += bet.amount
                    bet.creator.save()
                if bet.opponent:
                    bet.opponent.balance += bet.amount
                    bet.opponent.save()
            bet.arbiter_has_changed_status = True
            bet.save()
            return redirect('bets:bet_detail', bet.id)
    else:
        form = BetStatusForm(instance=copy.copy(bet))
    return render(request, 'bets/change_status.html',
                  {'form': form, 'bet': bet})


class BetListView(ListView):
    model = Bet
    template_name = 'bets/bet_list.html'
    context_object_name = 'bets'
    paginate_by = 30

    def get_queryset(self):
        status = self.request.GET.get('status', 'open')
        if status == 'all':
            return Bet.objects.all()
        return Bet.objects.filter(status=status)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_status'] = self.request.GET.get('status', 'open')
        context['status_choices'] = {
            'all': 'Все пари', **dict(Bet.STATUS_CHOICES)
        }
        return context


def bet_detail(request, bet_id):
    bet = get_object_or_404(Bet, id=bet_id)
    form = AcceptBetForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = request.user
        if bet.opponent is not None:
            form.add_error(None, "У этой ставки уже есть соперник.")
        elif bet.creator == user:
            form.add_error(None, "Вы не можете принять собственную ставку.")
        elif bet.status != 'open':
            form.add_error(None, "Ставка больше не открыта.")
        elif user.balance < bet.amount:
            form.add_error(None, "Недостаточно средств на балансе.")
        else:
            user.balance -= bet.amount
            user.save()
            bet.opponent = user
            bet.save()
            return redirect('bets:bet_detail', bet_id=bet.id)
    return render(request, 'bets/bet_detail.html', {'bet': bet, 'form': form})


@login_required
def profile_view(request):
    user = request.user
    user_bets = (Bet.objects.filter(creator=user)
                 | Bet.objects.filter(opponent=user))
    challenge_thrown_bets = Bet.objects.filter(opponent=user, status='open')
    arbitrated_bets = Bet.objects.filter(arbiter=user)
    if request.method == 'POST':
        form = BetForm(request.POST, user=request.user)
        if form.is_valid():
            bet = form.save(commit=False)
            bet.creator = user
            bet.save()
            return redirect('profile')
    else:
        form = BetForm(user=request.user)
    context = {
        'user': user,
        'bets': user_bets,
        'challenge_thrown_bets': challenge_thrown_bets,
        'arbitrated_bets': arbitrated_bets,
        'form': form,
    }
    return render(request, 'user/profile.html', context)


@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserForm(instance=request.user)
    return render(request, 'user/edit_profile.html',
                  {'form': form, 'balance': user.balance})
