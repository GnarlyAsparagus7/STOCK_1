# inventory/views.py

import csv
import logging

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.db.models import Sum
from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .models import (
    Product, Sale, SalesSummary, Purchase, PurchaseSummary,
    Expense, ExpenseSummary, ExpenseByCategory, Profile,
    InventoryLevel, ProfitMargin, SalesTrend, Notification, User
)
from .serializers import (
    ProductSerializer, SaleSerializer, SalesSummarySerializer,
    PurchaseSerializer, PurchaseSummarySerializer, UserSerializer,
    ExpenseSerializer, ExpenseSummarySerializer, ExpenseByCategorySerializer,
    LoginSerializer, InventoryLevelSerializer, ProfitMarginSerializer,
    SalesTrendSerializer, UserProfileSerializer, NotificationSerializer
)
from .permissions import IsAdmin, IsStaff, IsRegularUser

User = get_user_model()  # Use get_user_model to fetch the User model dynamically
logger = logging.getLogger(__name__)

# Home View
def home(request):
    return HttpResponse("Welcome to the Inventory Management System!")

# Test User Profile
def test_user_profile(request):
    try:
        user = User.objects.get(username='testuser')
        return HttpResponse(f"User profile found: {user.profile}")
    except User.DoesNotExist:
        return HttpResponse("User does not exist.")
    except Profile.DoesNotExist:
        return HttpResponse("Profile does not exist for this user.")

# ViewSets for CRUD operations
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        print("Received data:", request.data)  # Add this line for debugging
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("Validation errors:", serializer.errors)  # Add this line for debugging
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        product = self.get_object()
        response = super().update(request, *args, **kwargs)
        check_stock_levels(product)  # Check stock levels after the update
        return response

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        print("Sending data:", serializer.data)  # Add this line for debugging
        return Response(serializer.data)

class StaffProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsStaff]

class RegularUserProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsRegularUser]

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [permissions.AllowAny]

class SalesSummaryViewSet(viewsets.ModelViewSet):
    queryset = SalesSummary.objects.all()
    serializer_class = SalesSummarySerializer
    permission_classes = [permissions.AllowAny]

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [permissions.AllowAny]  # Changed from IsAuthenticated to AllowAny

class PurchaseSummaryViewSet(viewsets.ModelViewSet):
    queryset = PurchaseSummary.objects.all()
    serializer_class = PurchaseSummarySerializer
    permission_classes = [permissions.AllowAny]  # Changed from IsAuthenticated to AllowAny

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.AllowAny]  # Changed from IsAuthenticated to AllowAny

class ExpenseSummaryViewSet(viewsets.ModelViewSet):
    queryset = ExpenseSummary.objects.all()
    serializer_class = ExpenseSummarySerializer
    permission_classes = [permissions.AllowAny]  # Changed from IsAuthenticated to AllowAny

class ExpenseByCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExpenseByCategory.objects.all()
    serializer_class = ExpenseByCategorySerializer
    permission_classes = [permissions.AllowAny]  # Changed from IsAuthenticated to AllowAny

# User Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        Profile.objects.get_or_create(user=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# User Login View
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({'error': 'Invalid credentials'}, status=400)

        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=400)

# User ViewSet for listing and retrieving users
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

# Sales Summary View
class SalesSummaryView(generics.ListAPIView):
    queryset = SalesSummary.objects.all()
    serializer_class = SalesSummarySerializer

class PurchaseSummaryView(generics.ListAPIView):
    queryset = PurchaseSummary.objects.all()
    serializer_class = PurchaseSummarySerializer

class InventoryLevelsView(generics.ListAPIView):
    queryset = InventoryLevel.objects.all()
    serializer_class = InventoryLevelSerializer

class ExpensesByCategoryView(generics.ListAPIView):
    queryset = ExpenseByCategory.objects.all()
    serializer_class = ExpenseByCategorySerializer

class ProfitMarginsView(generics.ListAPIView):
    queryset = ProfitMargin.objects.all()
    serializer_class = ProfitMarginSerializer

class SalesTrendsView(generics.ListAPIView):
    queryset = SalesTrend.objects.all()
    serializer_class = SalesTrendSerializer

class UserProfileView(APIView):
    permission_classes = [permissions.AllowAny]

    def put(self, request):
        user = request.user
        serializer = UserProfileSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

class SalesReportView(APIView):
    def get(self, request):
        try:
            # Use 'totalAmount' instead of 'amount' to match your Sale model
            sales_data = Sale.objects.values('product__name').annotate(
                total_sales=Sum('totalAmount')
            )
            
            # If no sales data exists, return sample data for testing
            if not sales_data:
                # Sample data for testing
                sample_data = [
                    {'product__name': 'iPhone 21', 'total_sales': 1200},
                    {'product__name': 'Samsung Galaxy', 'total_sales': 1000},
                    {'product__name': 'Google Pixel', 'total_sales': 800},
                ]
                return Response({
                    'sales_data': sample_data,
                    'total_sales': sum(item['total_sales'] for item in sample_data)
                })
            
            total_sales = sum(item['total_sales'] for item in sales_data)
            return Response({
                'sales_data': sales_data,
                'total_sales': total_sales
            })
        except Exception as e:
            print(f"Error in SalesReportView: {str(e)}")  # For debugging
            return Response(
                {'error': 'Failed to generate sales report'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return self.queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

def check_stock_levels(product):
    if product.stock_quantity < 10:
        Notification.objects.create(
            user=product.user,
            message=f"Low stock alert for {product.name}. Only {product.stock_quantity} left."
        )

class ImportProductsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        file = request.FILES['file']
        reader = csv.DictReader(file.read().decode('utf-8').splitlines())
        errors = []

        for row in reader:
            try:
                product = Product(
                    name=row['name'],
                    price=float(row['price']),
                    stock_quantity=int(row['stock_quantity']),
                    rating=float(row.get('rating', 0))
                )
                product.full_clean()
                product.save()
            except (ValidationError, ValueError) as e:
                errors.append(f"Error importing product: {row['name']} - {str(e)}")

        if errors:
            return Response({'errors': errors}, status=400)
        return Response({'message': 'Products imported successfully!'}, status=201)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        users = self.get_queryset()
        user_data = [{"id": user.id, "email": user.email} for user in users]
        return Response(user_data)

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
