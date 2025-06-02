from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from bets.models import Bet
from .serializers import BetSerializer
from .permissions import IsAuthorOrReadOnly


class BetViewSet(viewsets.ModelViewSet):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly
    )

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=True,
            methods=['post'],
            permission_classes=(permissions.IsAuthenticated,))
    def accept(self, request, pk=None):
        bet = self.get_object()
        if bet.opponent is not None:
            return Response({'detail': 'Пари уже принято другим пользователем.'},
                            status=status.HTTP_400_BAD_REQUEST)
        if bet.creator == request.user:
            return Response({'detail': 'Нельзя принимать своё собственное пари.'},
                            status=status.HTTP_400_BAD_REQUEST)
        bet.opponent = request.user
        bet.status = 'accepted'
        bet.save()
        return Response({'status': 'Пари принято'}, status=status.HTTP_200_OK)
