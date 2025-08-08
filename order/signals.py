from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Order

@receiver(post_save, sender=Order)
def multipurpose_order_status_signal(sender, instance, **kwargs):
    """
    Multipurpose signal: always triggers on Order save and updates pet availability for all status transitions.
    - If status is 'Canceled', associated pets are made available.
    - If status is 'Delivered', pets remain unavailable (adopted).
    - For 'Pending', 'Ready To Ship', 'Shipped', pets are made unavailable.
    """
    if instance.status in[ Order.CANCELED, Order.READY_TO_SHIP]:
        for item in instance.items.select_related('pet').all():
            item.pet.mark_available()
    elif instance.status in [ Order.READY_TO_SHIP, Order.SHIPPED,Order.DELIVERED]:
        for item in instance.items.select_related('pet').all():
            item.pet.mark_unavailable()
    # For DELIVERED, do nothing (pets remain unavailable/adopted)

@receiver(post_delete, sender=Order)
def multipurpose_order_delete_signal(sender, instance, **kwargs):
    """
    Signal to make pets available again when an order is deleted.
    This ensures that if an admin deletes an order, the pet isn't stuck
    in an 'unavailable' state.
    """
    for item in instance.items.select_related('pet').all():
        item.pet.mark_available()
