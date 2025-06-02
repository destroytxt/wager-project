from django import forms
from django.utils import timezone

from .models import Bet, User


class BetForm(forms.ModelForm):
    class Meta:
        model = Bet
        fields = ('opponent', 'description', 'amount', 'deadline')

        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_deadline(self):
        deadline = self.cleaned_data.get('deadline')
        if deadline and deadline < timezone.now():
            raise forms.ValidationError("Срок пари не может быть в прошлом.")
        return deadline


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
