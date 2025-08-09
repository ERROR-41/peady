from rest_framework import serializers
from .models import TransactionHistory

class TransactionHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionHistory
        fields = ['id', 'user', 'transaction_type', 'amount', 'balance_after', 'order', 'created_at']
        read_only_fields = fields
