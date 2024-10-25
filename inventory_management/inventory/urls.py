# inventory/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import (
    ProductViewSet,
    SaleViewSet,
    SalesSummaryViewSet,
    PurchaseViewSet,
    PurchaseSummaryViewSet,
    UserViewSet,
    ExpenseViewSet,
    ExpenseSummaryViewSet,
    ExpenseByCategoryViewSet,
    RegisterView,
    LoginView,
    test_user_profile,
    SalesSummaryView,
    PurchaseSummaryView,
    InventoryLevelsView,
    UserProfileView,
    CustomAuthToken,
    SalesReportView,
    NotificationViewSet,
    ImportProductsView,
    UserListView
)
from inventory.models import User, Profile

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'sales', SaleViewSet)
router.register(r'sales_summary', SalesSummaryViewSet)
router.register(r'purchases', PurchaseViewSet)
router.register(r'purchase_summary', PurchaseSummaryViewSet)
router.register(r'users', UserViewSet)
router.register(r'expenses', ExpenseViewSet)
router.register(r'expense_summary', ExpenseSummaryViewSet)
router.register(r'expense_by_category', ExpenseByCategoryViewSet)
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('', include(router.urls)),  # This includes all registered routes
    path('register/', RegisterView.as_view(),
         name='register'),  # Registration endpoint
    path('login/', LoginView.as_view(), name='login'),  # Login endpoint
    path('reports/', include([
        path('sales-summary/', SalesSummaryView.as_view(), name='sales-summary'),
        path('purchase-summary/', PurchaseSummaryView.as_view(), name='purchase-summary'),
        path('inventory-levels/', InventoryLevelsView.as_view(), name='inventory-levels'),
    ])),
    path('profile/',UserProfileView.as_view(), name = 'user-profile'),
    path('api/token/', CustomAuthToken.as_view(), name='api_token'),
    path('api/import-products/', ImportProductsView.as_view(), name='import-products'),  # New import endpoint
    path('api/sales-report/', SalesReportView.as_view(), name='sales-report'),
    path('api/notifications/', NotificationViewSet.as_view(
        {'get': 'list', 'post': 'create'}), name='notification-list'),
    path('api/users/', UserListView.as_view(), name='user-list'),  # New endpoint to list users
]
