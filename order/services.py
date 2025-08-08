from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError
from .models import Cart, Order, OrderItem
from users.models import AccountBalance # Assuming this model exists

class OrderService:
    @staticmethod
    @transaction.atomic
    def create_order(user, cart_id):
        """
        Creates an order from a user's cart.
        The initial status is set to 'Ready To Ship'. The post_save signal will
        automatically handle marking the pets as unavailable.
        """
        try:
            cart = Cart.objects.select_related('user').get(pk=cart_id, user=user)
        except Cart.DoesNotExist:
            raise ValidationError("Invalid cart or permission denied.")

        cart_items = cart.items.select_related('pet').all()
        if not cart_items.exists():
            raise ValidationError("Cannot create an order from an empty cart.")

        # Check if any pets in the cart are already unavailable
        unavailable_pets = [item.pet.name for item in cart_items if not item.pet.availability_status]
        if unavailable_pets:
            raise ValidationError(f"The following pets are no longer available: {', '.join(unavailable_pets)}.")

        total_price = sum(item.pet.price for item in cart_items)

        # Handle payment/balance deduction
        # (Assuming a simple AccountBalance model on the user)
        try:
            account = AccountBalance.objects.get(user=user)
            if account.balance < total_price:
                raise ValidationError("Insufficient balance.")
            account.balance -= total_price
            account.save()
        except AccountBalance.DoesNotExist:
            raise ValidationError("User account balance not found.")

        # Create the order. The signal will handle pet availability.
        order = Order.objects.create(user=user, total_price=total_price, status=Order.READY_TO_SHIP)
        # Create the corresponding order items
        order_items_to_create = []
        for item in cart_items:
            order_item = OrderItem(order=order, pet=item.pet, price=item.pet.price, total_price=item.pet.price)
            order_items_to_create.append(order_item)
            # Mark pet as unavailable
            item.pet.mark_unavailable()
        OrderItem.objects.bulk_create(order_items_to_create)
        # The cart has been processed and can be deleted
        cart.delete()
        return order

    @staticmethod
    @transaction.atomic
    def cancel_order(order, user):
        """
        Cancels an order and refunds the user.
        The post_save signal will automatically make the pets available again.
        """
        if not (user.is_staff or order.user == user):
            raise PermissionDenied("You do not have permission to cancel this order.")

        if order.status in [Order.DELIVERED, Order.SHIPPED]:
            raise ValidationError("Cannot cancel an order that has already been shipped or delivered.")
        
        if order.status == Order.CANCELED:
            raise ValidationError("This order has already been canceled.")
            
        # Refund the total price to the user's account balance
        account, _ = AccountBalance.objects.get_or_create(user=order.user)
        account.balance += order.total_price
        account.save()
            
        # Update the order status. The signal will handle the rest.
        order.status = Order.CANCELED
        order.save()
        return order

    @staticmethod
    def mark_pets_unavailable(order):
        """
        Marks all pets in the order as unavailable.
        """
        for item in order.items.select_related('pet').all():
            item.pet.availability_status = False
            item.pet.save(update_fields=['availability_status'])

    @staticmethod
    def mark_pets_available(order):
        """
        Marks all pets in the order as available.
        """
        for item in order.items.select_related('pet').all():
            item.pet.availability_status = True
            item.pet.save(update_fields=['availability_status'])