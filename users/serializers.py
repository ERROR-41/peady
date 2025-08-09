from djoser.serializers import UserCreateSerializer
from rest_framework.serializers import ModelSerializer
from users.models import User, AccountBalance
from rest_framework import serializers
from decimal import Decimal
from order.serializers import OrderItemSerializer
from rest_framework import status
import time




class UserCreateSerializers(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["id", "email", "password"]


class UserBalanceSerializer(ModelSerializer):
    class Meta:
        model = AccountBalance
        fields = ["id", "balance", "add_money", "created_at", "updated_at"]
        read_only_fields = ["id", "balance", "add_money", "created_at", "updated_at"]


class AddBalanceSerializer(ModelSerializer):

    amount = serializers.DecimalField(max_digits=10, decimal_places=2, write_only=True, required=True)
    pin = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = AccountBalance
        fields = ["id", "amount", "balance", "add_money", "pin"]
        read_only_fields = ["id", "balance", "add_money"]

    def create(self, validated_data):
        amount = validated_data.pop("amount", None)
        pin = validated_data.pop("pin", None)
        if amount is None:
            raise serializers.ValidationError({"amount": "This field is required."})
        if pin is None:
            raise serializers.ValidationError({"pin": "PIN is required for add balance."})
        if amount < Decimal("100.00"):
            raise serializers.ValidationError({"amount": "Amount must be at least 100."})
        if amount < 0:
            raise serializers.ValidationError({"amount": "Negative amounts are not allowed."})
        user = self.context["request"].user
        if not hasattr(user, 'pin') or str(user.pin) != str(pin):
            raise serializers.ValidationError({"pin": "Invalid PIN."})
        account_balance, _ = AccountBalance.objects.get_or_create(user=user)
        account_balance.balance += amount
        account_balance.add_money += amount
        account_balance.save()
        # Return the account_balance instance for the view to handle the response
        return account_balance

    def update(self, instance, validated_data):
        # Handle the update logic here
        return instance
    
    

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
