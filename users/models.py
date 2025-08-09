from django.db import models
from django.contrib.auth.models import AbstractUser
from order.models import Order
from users.managers import CustomUserManager
from uuid import uuid4
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True)
    address = models.TextField(max_length=40, blank=True, null=True)
    phone_number = models.TextField(max_length=15, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    pin = models.CharField(max_length=10, default="1234")  # Default PIN is '1234'
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class AccountBalance(models.Model):
    add_money = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="accountbalance",
    )

    def __str__(self):
        return f"AccountBalance(id={self.id}, balance={self.balance})"



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_account_balance(sender, instance, created, **kwargs):
    if created:
        AccountBalance.objects.create(user=instance)
