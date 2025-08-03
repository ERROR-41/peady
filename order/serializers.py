from rest_framework import serializers
from order.models import Cart, CartItem, Order, OrderItem
from pet.models import Pet
# Removed unused import
from order.services import OrderService


class EmptySerializer(serializers.Serializer):
    pass


class SimplePetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ['id', 'name', 'price']


class AddCartItemSerializer(serializers.ModelSerializer):
    pet_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ['pet_id'] 

    def save(self):
        cart_id = self.context['cart_id']
        pet_id = self.validated_data['pet_id']

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, pet_id=pet_id)# If pet already exists, raise validation error since each pet should be unique
            raise serializers.ValidationError("This pet is already in your cart")
        except CartItem.DoesNotExist:
            # Create new cart item since pet doesn't exist in cart
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)
        return self.instance

    def validate_pet_id(self, value):
        if not Pet.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                f"Pet with id {value} does not exist")
        
        # Check if pet is available for adoption
        pet = Pet.objects.get(pk=value)
        if  pet.availability_status == False:
            raise serializers.ValidationError(
                f"Pet '{pet.name}' is not available for adoption")
        
        return value


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'pet_id']


class CartItemSerializer(serializers.ModelSerializer):
    pet = SimplePetSerializer()
    total_price = serializers.SerializerMethodField(
        method_name='get_total_price')

    class Meta:
        model = CartItem
        fields = ['id', 'pet', 'total_price']

    def get_total_price(self, cart_item: CartItem):
        return cart_item.pet.price


class CartSerializer(serializers.ModelSerializer):

    def get_total_price(self, cart):
        return sum(item.pet.price for item in cart.items.all())
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(
        method_name='get_total_price')

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']
        read_only_fields = ['user']


    def create(self, validated_data):
        user = self.context['request'].user
        if Cart.objects.filter(user=user).exists():
            existing_cart = Cart.objects.get(user=user)
            raise serializers.ValidationError({
                "detail": "A cart already exists for this user.",
                "existing_cart_id": str(existing_cart.id)
            })
        validated_data['user'] = user
        return super().create(validated_data)
    


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No cart found with this id')

        if not CartItem.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError('Cart is empty')

        # Check if all pets in the cart are still available
        cart_items = CartItem.objects.filter(cart_id=cart_id).select_related('pet')
        unavailable_pets = []
        
        for item in cart_items:
            if not item.pet.availability_status:
                unavailable_pets.append(item.pet.name)
        
        if unavailable_pets:
            pets_list = ", ".join(unavailable_pets)
            raise serializers.ValidationError(
                f"The following pets are no longer available: {pets_list}. "
                "Please remove them from your cart before placing the order."
            )

        return cart_id

    def create(self, validated_data):
        user_id = self.context['user_id']
        cart_id = validated_data['cart_id']

        try:
            order = OrderService.create_order(user_id=user_id, cart_id=cart_id)
            return order
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def to_representation(self, instance):
        return OrderSerializer(instance).data
    
    

class OrderItemSerializer(serializers.ModelSerializer):
    pet = SimplePetSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'pet', 'price', 'total_price']


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']


class OrderSerializer(serializers.ModelSerializer):

    items = OrderItemSerializer(many=True)
    all_pet_price = serializers.SerializerMethodField()

    def get_all_pet_price(self, obj):
        return sum(item.pet.price for item in obj.items.all())

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total_price', 'created_at', 'items', 'all_pet_price']
