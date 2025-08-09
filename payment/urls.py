from rest_framework.routers import DefaultRouter
from .views import TransactionHistoryViewSet

router = DefaultRouter()
router.register(r'transactions', TransactionHistoryViewSet, basename='transactionhistory')

urlpatterns = router.urls
