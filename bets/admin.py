from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Bet


User = get_user_model()


@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'creator',
        'opponent',
        'status',
        'description',
        'amount',
        'created_at'
    )
    list_filter = ('status', 'created_at')
    search_fields = ('creator__username', 'opponent__username')
    ordering = ('-created_at',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'balance', 'date_joined')
    search_fields = ('username', 'email')
