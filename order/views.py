from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from order import serializers as orderSz
from order.serializers import CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer
from order.models import Cart, CartItem, Order, OrderItem
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from order.services import OrderService
from rest_framework.response import Response


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    """
    CartViewSet handles CRUD operations for the Cart model for authenticated users.
    API Endpoints:
        - create (POST): Create a new cart for the authenticated user.
        - retrieve (GET): Retrieve the cart details for the authenticated user.
        - destroy (DELETE): Delete the cart for the authenticated user.
    Permissions:
        - Only authenticated users can access these endpoints.
     Notes:
        - When generating API documentation (e.g., with Swagger), returns an empty queryset to avoid errors.
    """
    
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()
        return Cart.objects.prefetch_related('items__pet').filter(user=self.request.user)


class CartItemViewSet(ModelViewSet):
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        # Calculate total price of all pets in the cart
        all_pet_price = sum(item.pet.price for item in queryset)
        return Response({
            'items': serializer.data,
            'all_pet_price': all_pet_price
        })
    """
    API endpoint that allows users to view, add, update, and delete items in a shopping cart.
    This viewset provides the following actions for cart items:
    - `list`: Retrieve all items in a specific cart.
    - `create`: Add a new item to the cart.
    - `partial_update`: Update the quantity or details of an existing cart item.
    - `destroy`: Remove an item from the cart.
    Permissions:
        - Only authenticated users can access these endpoints.
    
    """
    
    
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            return context

        return {'cart_id': self.kwargs.get('cart_pk')}

    def get_queryset(self):
        return CartItem.objects.select_related('pet').filter(cart_id=self.kwargs.get('cart_pk'))


class OrderViewset(ModelViewSet):
    """
    OrderViewset handles CRUD operations and custom actions for Order objects in the Pet Adoptions system.
    Standard Endpoints:
    - list: Retrieve a list of orders. Admins see all orders; regular users see their own.
    - retrieve: Retrieve details of a specific order.
    - create: Place a new order for pet adoption.
    - destroy: Delete an order (admin only).
    - partial_update: Partially update an order (admin only).
    Custom Actions:
    - cancel (POST /orders/{id}/cancel/): Cancel an order. Only the order owner can cancel.
    - update_status (PATCH /orders/{id}/update_status/): Update the status of an order (admin only).
    Queryset:
    - Admins see all orders; regular users see only their own orders.
    """
    http_method_names = ['get', 'post', 'delete', 'patch', 'head', 'options']

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        OrderService.cancel_order(order=order, user=request.user)
        return Response({'status': 'Canceled'})
    
    @action(detail=True, methods=['post'])
    def mark_as_delivered(self, request, pk=None):
        order = self.get_object()
        if order.status != 'Delivered':
            return Response({'error': 'Order is not marked as delivered yet.'}, status=400)

        # Save order details to user's pet adoption history only if status is 'delivered'
        user = request.user
        for item in order.items.all():
            user.pet_adoption_history.create(
                pet=item.pet,
                adoption_date=order.updated_at,
                order_id=order.id
            )

        return Response({'status': 'Order marked as delivered and saved to pet adoption history.'})
    
    
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        order = self.get_object()
        serializer = orderSz.UpdateOrderSerializer(
            order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'status': f'Order status updated to {request.data['status']}'})

    def get_permissions(self):
        if self.action in ['update_status', 'destroy']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'cancel':
            return orderSz.EmptySerializer
        if self.action == 'create':
            return orderSz.CreateOrderSerializer
        elif self.action == 'update_status':
            return orderSz.UpdateOrderSerializer
        return orderSz.OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user)
        # Mark pets as unavailable after order creation
        for item in order.items.all():
            pet = item.pet
            pet.available = False
            pet.save()

    def perform_update(self, serializer):
        order = serializer.save()
        # If status is set to 'canceled', mark pets as available again
        if hasattr(order, 'status') and order.status == 'canceled':
            for item in order.items.all():
                pet = item.pet
                pet.available = True
                pet.save()

    def perform_destroy(self, instance):
        # When an order is deleted (including cancel), mark pets as available again
        for item in instance.items.all():
            pet = item.pet
            pet.available = True
            pet.save()
        instance.delete()

    def get_serializer_context(self):
        if getattr(self, 'swagger_fake_view', False):
            return super().get_serializer_context()
        return {'user_id': self.request.user.id, 'user': self.request.user}

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('items__pet').all()
        return Order.objects.prefetch_related('items__pet').filter(user=self.request.user)
