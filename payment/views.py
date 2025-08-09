from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import TransactionHistory
from .serializers import TransactionHistorySerializer


class TransactionHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TransactionHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TransactionHistory.objects.filter(user=self.request.user).order_by("-created_at")

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        serializer = self.get_serializer(qs, many=True)
        return Response({
            "count": qs.count(),
            "results": serializer.data,
        })