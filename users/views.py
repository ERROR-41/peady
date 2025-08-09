from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from users.models import User
from users.serializers import AddBalanceSerializer, UserProfileSerializer
from rest_framework import permissions
from decimal import Decimal
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.decorators import action


class UserProfileViewSet(ModelViewSet):
    """
    A viewset for viewing and editing user profile instances.
    This viewset provides the following functionality:
    - Allows authenticated users to view their own profile details.
    - Restricts profile creation, update, and deletion to admin users only.
    - Uses the `UserProfileSerializer` for serialization.
    - Applies appropriate permissions based on the action being performed.
    Permissions:
        - Authenticated users can view profiles.
        - Only admin users can create, update, or delete profiles.

    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "put", "patch", "delete"]

    

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

def action(self, request, *args, **kwargs):
    raise NotImplementedError


class AccountBalanceViewSet(ModelViewSet):

   
    """
    API endpoint that allows users to add money to their account balance.                   
    - partial_update: Partially update the user's account balance. (Authenticated users only)       
    - retrieve: Retrieve details of the user's account balance. (Authenticated users only)  
    """
    
    serializer_class = AddBalanceSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post"]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        account_balance = serializer.save()
        user = request.user
        return Response({
            'owner_name': user.get_full_name() or user.email,
            'message': 'Money deposited successfully.',
            'added_amount': str(request.data.get('amount')),
            'new_balance': str(account_balance.balance),
            'total_added_money': str(account_balance.add_money),
            'account_id': str(account_balance.id),
        })
    
    
        
    def list(self, request, *args, **kwargs):
        user = request.user
        account = user.accountbalance
        return Response({
            'Id': str(account.id),
            'User FullName': user.get_full_name() or user.email,
            'current_balance': str(account.balance),
            'total_added_money': str(account.add_money),
        })


