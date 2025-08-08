from django.db import models
from django.conf import settings
from uuid import uuid4
from pet.models import Pet


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart of {self.user.get_full_name() }"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

    class Meta:
        unique_together = [['cart', 'pet']]

    def __str__(self):
        return f"{self.pet.name} in cart {self.cart.id}"


class Order(models.Model):
    PENDING = "Pending"
    READY_TO_SHIP = "Ready To Ship"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"
    CANCELED = "Canceled"
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (READY_TO_SHIP, "Ready To Ship"),
        (SHIPPED, "Shipped"),
        (DELIVERED, "Delivered"),
        (CANCELED, "Canceled"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.get_full_name()} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.pet.name} (Order {self.order.id})"
