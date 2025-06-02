from rest_framework import serializers
from bets.models import Bet


class BetSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    opponent = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    winner = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Bet
        fields = '__all__'
        read_only_fields = ('status', 'creator', 'winner', 'opponent')
