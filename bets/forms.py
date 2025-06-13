from django import forms
from django.utils import timezone

from .models import Bet, User


class AcceptBetForm(forms.Form):
    pass


class BetForm(forms.ModelForm):
    class Meta:
        model = Bet
        fields = ('opponent', 'description', 'amount', 'deadline', 'arbiter')
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['opponent'].queryset = User.objects.exclude(id=self.user.id)
        if not self.data.get('arbiter') and not self.instance.arbiter_id:
            self.fields['arbiter'].initial = (
                User.objects.filter(is_superuser=True).first())

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline and deadline < timezone.now():
            raise forms.ValidationError("Срок пари не может быть в прошлом.")
        return deadline

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('opponent') == self.user:
            self.add_error('opponent', "Нельзя заключать пари с самим собой.")


class BetStatusForm(forms.ModelForm):
    class Meta:
        model = Bet
        fields = ('status', 'winner')
        labels = {
            'status': 'Статус пари',
            'winner': 'Победитель (если завершено)'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        allowed_statuses = ('finished', 'cancelled')
        self.fields['status'].choices = [
            choice for choice in self.fields['status'].choices
            if choice[0] in allowed_statuses
        ]
        bet = self.instance
        user_ids = [bet.creator.pk]
        if bet.opponent:
            user_ids.append(bet.opponent.pk)
        self.fields['winner'].queryset = User.objects.filter(pk__in=user_ids)

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        winner = cleaned_data.get('winner')
        if status == 'finished' and not winner:
            raise forms.ValidationError(
                'Если пари завершено, необходимо указать победителя.')
        if self.instance.arbiter_has_changed_status:
            raise forms.ValidationError(
                'Арбитр уже менял статус пари и не может сделать это снова.')


class UserForm(forms.ModelForm):
    balance = forms.DecimalField(disabled=True, required=False, label='Баланс')
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Дата рождения'
    )

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'bio',
            'birth_date',
            'email',
            'balance'
        )
