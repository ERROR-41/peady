from rest_framework.viewsets import ModelViewSet
from pet.serializer import (
    PetImageSerializer,
    CategorySerializer,
    ReviewSerializer,
    PetSeralizer,
)
from pet.models import Pet, PetImage, Review, Category
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend




class PetAdoptionViewSet(ModelViewSet):
    """
    API endpoint that allows pets to be viewed or edited.
    - list: Retrieve a list of all pets. Supports filtering by category.
    - retrieve: Retrieve details of a specific pet by ID.
    - create: Add a new pet to the adoption list. (Admin only)
    - update: Update an existing pet's information. (Admin only)
    - partial_update: Partially update a pet's information. (Admin only)
    - destroy: Remove a pet from the adoption list. (Admin only)
    """

    serializer_class = PetSeralizer
    queryset = Pet.objects.select_related("category").all()
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [permissions.IsAdminUser]
        else:
            self.permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return super().get_permissions()

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category"]


class PetImageViewSet(ModelViewSet):
    """
    API endpoint that allows pet images to be viewed or edited.
    - list: Retrieve a list of all images for a specific pet.
    - retrieve: Retrieve a specific image by ID.
    - create: Add a new image for a pet. (Admin only)
    - update: Update an existing image. (Admin only)
    - destroy: Remove an image. (Admin only)
    """

    serializer_class = PetImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        pets_pk = self.kwargs.get("pets_pk")
        if not pets_pk:
            return PetImage.objects.none()
        return PetImage.objects.filter(pet_id=pets_pk)

    def perform_create(self, serializer):
        pets_pk = self.kwargs.get("pets_pk")
        if pets_pk:
            serializer.save(pet_id=pets_pk)

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [permissions.IsAdminUser]
        else:
            self.permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return super().get_permissions()


class PetCategoryViewSet(ModelViewSet):
    """
    API endpoint that allows pet categories to be viewed or edited.
    - list: Retrieve a list of all pet categories.
    - retrieve: Retrieve details of a specific pet category by ID.
    - create: Add a new pet category. (Admin only)
    - update: Update an existing pet category. (Admin only)
    - partial_update: Partially update a pet category. (Admin only)
    - destroy: Remove a pet category. (Admin only)
    """

    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [permissions.IsAdminUser]
        else:
            self.permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        return super().get_permissions()


class ReviewViewSet(ModelViewSet):
    """
    API endpoint that allows pet reviews to be viewed or edited.
    - list: Retrieve a list of all reviews for a specific pet.
    - retrieve: Retrieve details of a specific review by ID.
    - create: Add a new review for a specific pet. (Authenticated users only)
    - update: Update an existing review. (Authenticated users only, can only update own reviews)
    - delete: Delete a review. (Authenticated users only, can only delete own reviews)
    """

    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.select_related("user", "pet").filter(
            pet_id=self.kwargs.get("pets_pk")
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["pet_id"] = self.kwargs.get("pets_pk")
        return context

    def destroy(self, request, *args, **kwargs):
        review = self.get_object()
        # Check if user is authorized to delete this review
        if review.user != request.user and not request.user.is_staff:
            return Response(
                {"detail": "You can only delete your own reviews"}, status=403
            )
        return super().destroy(request, *args, **kwargs)
