from order.models import Cart, CartItem, OrderItem, Order
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError
from users.models import AccountBalance

class OrderService:
    @staticmethod
    def create_order(user_id, cart_id):
        with transaction.atomic():
            cart = Cart.objects.get(pk=cart_id)
            cart_items = cart.items.select_related('pet').all()

            total_price = sum([item.pet.price *
                               item.quantity for item in cart_items])

            if not cart.user:
                raise ValidationError({"detail": "Cart is not associated with a valid user"})

            try:
                account_balance = AccountBalance.objects.get(user=cart.user)
                user_balance = account_balance.balance
                account_balance.balance -= total_price
                account_balance.save()    
                
            except AccountBalance.DoesNotExist:
                raise ValidationError({"detail": "User does not have an account balance"})

            if user_balance < total_price:
                raise ValidationError({"detail": "Insufficient balance to place the order"})
            
            
            order = Order.objects.create(
                user_id=user_id, total_price=total_price, status=Order.READY_TO_SHIP)

            order_items = [
                OrderItem(
                    order=order,
                    pet=item.pet,
                    price=item.pet.price,
                    quantity=item.quantity,
                    total_price=item.pet.price * item.quantity
                )
                for item in cart_items
            ]

            OrderItem.objects.bulk_create(order_items)

            cart.delete()

            return order

    @staticmethod
    def cancel_order(order, user):
        if user.is_staff:
            if order.status != Order.CANCELED:
                account_balance, _ = AccountBalance.objects.get_or_create(user=order.user)
                account_balance.balance += order.total_price
                account_balance.save()
            order.status = Order.CANCELED
            order.save()
            return order

        if order.user != user:
            raise PermissionDenied(
                {"detail": "You can only cancel your own order"})

        if order.status in [Order.DELIVERED, Order.SHIPPED]:
            raise ValidationError({"detail": "You cannot cancel an order that has been delivered or shipped"})

        if order.status != Order.CANCELED:
            account_balance, _ = AccountBalance.objects.get_or_create(user=order.user)
            account_balance.balance += order.total_price
            account_balance.save()

        order.status = Order.CANCELED
        order.save()
        return order


