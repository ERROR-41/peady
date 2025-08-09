from django.contrib import admin
from .models import TransactionHistory

@admin.register(TransactionHistory)
class TransactionHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_type', 'amount', 'balance_after', 'order', 'created_at')
    list_filter = ('transaction_type', 'created_at', 'user')
    search_fields = ('user__email', 'order__id')
