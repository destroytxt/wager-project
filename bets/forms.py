from django import forms
from django.utils import timezone

from .models import Bet, User


class BetForm(forms.ModelForm):
    class Meta:
        model = Bet
        fields = ('opponent', 'description', 'amount', 'deadline', 'arbiter')

        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        superuser = User.objects.filter(is_superuser=True).first()
        self.fields['arbiter'].initial = superuser

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline and deadline < timezone.now():
            raise forms.ValidationError("Срок пари не может быть в прошлом.")
        return deadline


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
        allowed_statuses = ('finished', 'cancelled', 'declined')
        self.fields['status'].choices = [
            choice for choice in self.fields['status'].choices
            if choice[0] in allowed_statuses
        ]
        bet = self.instance
        self.fields['winner'].queryset = User.objects.filter(
            pk__in=[bet.creator.pk, bet.opponent.pk])

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        winner = cleaned_data.get('winner')
        if status == 'finished' and not winner:
            self.add_error('winner', 'Если пари завершено,'
                                     ' необходимо указать победителя.')


class UserForm(forms.ModelForm):
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
            'balance',
            'bio',
            'birth_date',
            'email',
        )
