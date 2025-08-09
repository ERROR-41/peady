from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import AccountBalance
from order.models import Order
from payment.models import TransactionHistory

# Deposit (add_money)
@receiver(post_save, sender=AccountBalance)
def log_deposit(sender, instance, created, **kwargs):
    if created:
        # Initial creation, skip
        return
    # If add_money increased, log deposit
    if hasattr(instance, '_prev_add_money') and instance.add_money > instance._prev_add_money:
        TransactionHistory.objects.create(
            user=instance.user,
            transaction_type=TransactionHistory.DEPOSIT,
            amount=instance.add_money - instance._prev_add_money,
            balance_after=instance.balance
        )

# Payment (order creation)
@receiver(post_save, sender=Order)
def log_payment(sender, instance, created, **kwargs):
    if created and instance.total_price > 0:
        TransactionHistory.objects.create(
            user=instance.user,
            transaction_type=TransactionHistory.PAYMENT,
            amount=instance.total_price,
            balance_after=instance.user.accountbalance.balance,
            order=instance
        )

# Refund (order cancel)
@receiver(post_save, sender=Order)
def log_refund(sender, instance, **kwargs):
    if instance.status == Order.CANCELED and hasattr(instance, '_prev_status') and instance._prev_status != Order.CANCELED:
        TransactionHistory.objects.create(
            user=instance.user,
            transaction_type=TransactionHistory.REFUND,
            amount=instance.total_price,
            balance_after=instance.user.accountbalance.balance,
            order=instance
        )
