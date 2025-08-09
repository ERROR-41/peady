from django.shortcuts import render
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from order import serializers as orderSz
from order.serializers import CartSerializer, CartItemSerializer, AddCartItemSerializer, UpdateCartItemSerializer, OrderItemSerializer
from order.models import Cart, CartItem, Order, OrderItem
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from order.services import OrderService
from rest_framework.response import Response
from rest_framework import viewsets, permissions


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
    
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return orderSz.CartCreateSerializer
        return orderSz.CartSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
       
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'message': 'Cart is successfully created.',
            'cart': serializer.data
        }, status=201, headers=headers)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Cart.objects.none()
        return Cart.objects.prefetch_related('items__pet').filter(user=self.request.user)


class CartItemViewSet(ModelViewSet):

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({
            'message': 'Cart item created successfully.',
            'item': serializer.data
        }, status=201, headers=headers)
        
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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        cart = instance.cart
        self.perform_destroy(instance)
        # If the cart has no more items, delete the cart
        if cart.items.count() == 0:
            cart.delete()
            return Response({'message': 'Cart item removed successfully. Cart deleted because it is now empty.'})
        return Response({'message': 'Cart item removed successfully.'})


class OrderViewSet(ModelViewSet):
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
        try:
            OrderService.cancel_order(order=order, user=request.user)
            return Response({'status': 'Canceled'})
        except Exception as e:
            return Response({'error': str(e)}, status=400)
    
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
        if serializer.is_valid():
            serializer.save()
            return Response({'status': f"Order status updated to {serializer.validated_data.get('status', order.status)}"})
        return Response(serializer.errors, status=400)

    def get_permissions(self):
        # Only admin can change order status in any way
        if self.action in ['update_status', 'partial_update',  'mark_as_delivered']:
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
        # Use the service to create the order, not just serializer.save()
        user = self.request.user
        cart_id = serializer.validated_data.get('cart_id')
        order = OrderService.create_order(user=user, cart_id=cart_id)
        return order

    def perform_update(self, serializer):
        order = serializer.save()
        # If status is set to 'canceled', mark pets as available again
        if hasattr(order, 'status') and order.status == 'canceled':
            from order.services import OrderService
            OrderService.mark_pets_available(order)

    def perform_destroy(self, instance): 
        OrderService.mark_pets_available(instance)
        instance.delete()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            return context
        context.update({'user_id': self.request.user.id, 'user': self.request.user, 'request': self.request})
        return context

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        if self.request.user.is_staff:
            return Order.objects.prefetch_related('items__pet').all()
        return Order.objects.prefetch_related('items__pet').filter(user=self.request.user)

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['get',  'delete']

    def get_queryset(self):
        order_id = self.kwargs.get('order_id')
        base_qs = OrderItem.objects.filter(order__user=self.request.user)
        if order_id:
            return base_qs.filter(order_id=order_id)
        return base_qs

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)