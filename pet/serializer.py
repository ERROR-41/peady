from rest_framework.serializers import ModelSerializer
from pet.models import Pet, PetImage, Review, Category
from rest_framework import serializers
from django.contrib.auth import get_user_model


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]
        read_only_fields = ["id"]


class PetImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = PetImage
        fields = [ "image"]


class PetSeralizer(ModelSerializer):
    class Meta:
        model = Pet
        fields = [
            "id",
            "name",
            "category",
            "age",
            "category_name",
            "breed",
            "price",
             "availability_status",
            "description",
            "pet_images",
        ]
        read_only_fields = ["availability_status"]

    category_name = serializers.CharField(source="category.name", read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), write_only=True
    )
    
    pet_images = PetImageSerializer(source="images", many=True, read_only=True)

    

    def validate_availability_status(self, value):
        if value == 0:
            raise serializers.ValidationError("Availability status cannot False")





class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name="get_current_user_name")

    class Meta:
        model = get_user_model()
        fields = ["id", "name"]

    def get_current_user_name(self, obj):
        return obj.get_full_name()


class ReviewSerializer(serializers.ModelSerializer):
    user_details = serializers.SerializerMethodField(method_name="get_user_details")

    class Meta:
        model = Review
        fields = ["id", "user", "user_details",  "comments", "date"]
        read_only_fields = ["user", "date", ]

    def get_user_details(self, obj):
        return SimpleUserSerializer(obj.user).data

    def create(self, validated_data):
        pet_id = self.context["pet_id"]
        user = self.context["request"].user
        # Check if user already has a review for this pet
        existing_review = Review.objects.filter(pet_id=pet_id, user=user).first()
        if existing_review:
            raise serializers.ValidationError({"detail": "You have already reviewed this pet"})

        # Check if user has ordered (adopted) this pet
        from order.models import OrderItem
        has_ordered = OrderItem.objects.filter(pet_id=pet_id, order__user=user).exists()
        if not has_ordered:
            raise serializers.ValidationError({"detail": "You can only review pets you have adopted (ordered)."})

        return Review.objects.create(pet_id=pet_id, user=user, **validated_data)

    def validate(self, attrs):
        # Ensure only users who have adopted (ordered) the pet can post a review
        pet_id = self.context.get("pet_id")
        user = self.context["request"].user
        from order.models import OrderItem
        has_ordered = OrderItem.objects.filter(pet_id=pet_id, order__user=user).exists()
        if not has_ordered:
            raise serializers.ValidationError({"detail": "You can only review pets you have adopted (ordered)."})
        return attrs

    def update(self, instance, validated_data):
        # Ensure user can only update their own reviews
        if (
            instance.user != self.context["request"].user
            and not self.context["request"].user.is_staff
        ):
            raise serializers.ValidationError(
                {"detail": "You can only update your own reviews"}
            )
        return super().update(instance, validated_data)
