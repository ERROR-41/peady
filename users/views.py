
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from order.views import IsAuthenticated, action
from users.models import User
from users.serializers import AddBalanceSerializer, UserProfileSerializer
from rest_framework import permissions


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

    
