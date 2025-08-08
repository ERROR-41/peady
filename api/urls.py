from django.urls import path, include
from order.views import CartItemViewSet, CartViewSet,OrderViewSet
from pet.views import (
    PetAdoptionViewSet,
    PetCategoryViewSet,
    ReviewViewSet,
    PetImageViewSet,
)
from rest_framework_nested import routers
from users.views import UserProfileViewSet, AccountBalanceViewSet


router = routers.DefaultRouter()
router.register("pets", PetAdoptionViewSet, basename="pets")
router.register("categories", PetCategoryViewSet, basename="category")
router.register("carts", CartViewSet, basename="carts")
router.register("orders", OrderViewSet, basename="orders")
# Register the profile viewset (replace `ProfileViewSet` with the actual viewset for profiles)
router.register("profile", UserProfileViewSet, basename="profile")
router.register("add_money", AccountBalanceViewSet, basename="add_money")

pet_router = routers.NestedDefaultRouter(router, "pets", lookup="pets")
pet_router.register("reviews", ReviewViewSet, basename="pet-review")
pet_router.register("images", PetImageViewSet, basename="pet-images")

cart_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
cart_router.register("items", CartItemViewSet, basename="cart-item")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(cart_router.urls)),
    path("", include(pet_router.urls)),
]
