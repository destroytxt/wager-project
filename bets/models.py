from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=1,
        default=0,
        verbose_name='Баланс'
    )

    def __str__(self):
        return self.username


class Bet(models.Model):
    STATUS_CHOICES = [
        ('open', 'Открыто'),
        ('accepted', 'Принято'),
        ('finished', 'Завершено'),
        ('declined', 'Отклонено'),
        ('cancelled', 'Отменено'),
    ]

    creator = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='bets_created',
        verbose_name='Создатель пари'
    )
    opponent = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='bets_joined',
        verbose_name='Противник'
    )
    description = models.TextField(verbose_name='Описание пари')
    amount = models.DecimalField(
        max_digits=10, decimal_places=1,
        verbose_name='Сумма пари'
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES,
        default='open', verbose_name='Статус'
    )
    winner = models.ForeignKey(
        User, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='bets_won',
        verbose_name='Победитель'
    )
    deadline = models.DateTimeField(
        verbose_name='Срок пари',
        null=True, blank=True,
        help_text='Дата и время, до которого пари действует'
    )
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Дата создания')

    def __str__(self):
        return f'Пари #{self.id} — {self.creator} vs {self.opponent}'

    class Meta:
        ordering = ['-created_at']
