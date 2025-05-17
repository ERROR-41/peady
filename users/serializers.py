from djoser.serializers import UserCreateSerializer
from rest_framework.serializers import ModelSerializer
from users.models import User, AccountBalance
from rest_framework import serializers
from decimal import Decimal
from order.serializers import OrderItemSerializer



class UserCreateSerializers(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["id", "email", "password"]


class UserBalanceSerializer(ModelSerializer):
    class Meta:
        model = AccountBalance
        fields = ["id", "balance", "created_at", "updated_at"]
        read_only_fields = ["id", "balance", "created_at", "updated_at"]


class AddBalanceSerializer(ModelSerializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True)

    class Meta:
        model = AccountBalance
        fields = ["id", "amount", "balance"]
        read_only_fields = ["id", "balance"]

    def create(self, validated_data):
        amount = validated_data.pop("amount", Decimal("0.00"))
        if amount <= Decimal("0.00") or amount <= Decimal("100.00"):
            raise serializers.ValidationError(
                {"amount": "Amount must be greater than zero and greater than 100."}
            )
        account_balance, _ = AccountBalance.objects.get_or_create(
            user=self.context["request"].user
        )
        account_balance.balance += amount
        account_balance.save()
        return account_balance



class UserProfileSerializer(ModelSerializer):
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        account_balance = AccountBalance.objects.filter(user=instance).first()
        representation["balance"] = (
            account_balance.balance if account_balance else Decimal("0.00")
        )
        return representation

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
            "address",
            "balance" ,  
          
        ]
        read_only_fields = ["email", "last_login", "balance"]
