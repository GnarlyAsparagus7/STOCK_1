from rest_framework import serializers
from .models import Product, Sale, SalesSummary, Purchase, PurchaseSummary, User, Expense, ExpenseSummary, ExpenseByCategory, CustomUser, InventoryLevel, Notification

from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'rating', 'stock_quantity', 'user']


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = '__all__'


class SalesSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesSummary
        fields = '__all__'  # Correct usage to include all fields


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = '__all__'


class PurchaseSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseSummary
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'


class ExpenseSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseSummary
        fields = '__all__'


class ExpenseByCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseByCategory
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'password']

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            name=validated_data['name'],
        )
        user.set_password(validated_data['password'])  # Hash the password
        user.save()
        return user

class SalesSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesSummary
        fields = '__all__'  # Correct usage to include all fields
        
class PurchaseSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseSummary
        fields = ['id', 'product', 'quantity', 'unit_cost', 'timestamp']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)        
    
    
class InventoryLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryLevel
        fields = '__all__'  # Adjust fields as necessary


class ProfitMarginSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesSummary  # Assuming this is the model you want to use
        # Adjust fields as necessary
        fields = ['id', 'product', 'profit_margin']


class SalesTrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesSummary  # Assuming this is the model you want to use
        fields = ['timestamp', 'sales_amount']  # Adjust fields as necessary


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # Add any other fields you want to allow updates for
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get(
            'first_name', instance.first_name)
        instance.last_name = validated_data.get(
            'last_name', instance.last_name)
        instance.save()
        return instance


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'created_at', 'is_read']
