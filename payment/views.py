from rest_framework import viewsets, permissions
from .models import TransactionHistory
from .serializers import TransactionHistorySerializer

class TransactionHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TransactionHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TransactionHistory.objects.filter(user=self.request.user).order_by('-created_at')
