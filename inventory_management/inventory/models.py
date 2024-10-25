# inventory/models.py

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)  # Add this field

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
    
    # Add the required permissions methods
    def has_perm(self, perm, obj=None):
        return True  # Grant all permissions, adjust as needed

    def has_module_perms(self, app_label):
        return True  # Allow access to the module, adjust as needed

# 3. Reference the User model after CustomUser is defined
User = get_user_model()


# 4. Define the Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    # Removed bio field to avoid duplication since CustomUser already has it
    # Add other profile-specific fields if needed
    # For example:
    # address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.email


# 5. Signals to create and save Profile automatically
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# 6. Define other models after CustomUser and Profile
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField(null=True, blank=True)
    stock_quantity = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Sale(models.Model):
    saleId = models.CharField(max_length=255, primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateField()
    quantity = models.IntegerField()
    unitPrice = models.DecimalField(max_digits=10, decimal_places=2)
    totalAmount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Sale {self.saleId} of {self.product.name}"


class SalesSummary(models.Model):
    salesSummaryId = models.CharField(max_length=255, primary_key=True)
    totalValue = models.DecimalField(max_digits=10, decimal_places=2)
    changePercentage = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"Sales Summary {self.salesSummaryId} on {self.date}"


class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.name} purchased"


class PurchaseSummary(models.Model):
    purchaseSummaryId = models.CharField(max_length=255, primary_key=True)
    totalPurchased = models.DecimalField(max_digits=10, decimal_places=2)
    changePercentage = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"Purchase Summary {self.purchaseSummaryId} on {self.date}"


class Expense(models.Model):
    expenseId = models.CharField(max_length=255, primary_key=True)
    category = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateField()

    def __str__(self):
        return f"Expense {self.expenseId} in {self.category}"


class ExpenseSummary(models.Model):
    expenseSummaryId = models.CharField(max_length=255, primary_key=True)
    totalExpenses = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"Expense Summary {self.expenseSummaryId} on {self.date}"


class ExpenseByCategory(models.Model):
    expenseByCategoryId = models.CharField(max_length=255, primary_key=True)
    expenseSummary = models.ForeignKey(
        ExpenseSummary, on_delete=models.CASCADE)
    date = models.DateField()
    category = models.CharField(max_length=255)
    amount = models.BigIntegerField()

    def __str__(self):
        return f"Expense {self.expenseByCategoryId} in {self.category} on {self.date}"


class ProfitMargin(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    margin_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"Profit Margin for {self.product.name} on {self.date}"


class SalesTrend(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField()
    sales_quantity = models.IntegerField()
    sales_value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Sales Trend for {self.product.name} on {self.date}"

class InventoryLevel(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Assuming you have a Product model
    quantity = models.IntegerField()
    # Add other fields as necessary

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def __str__(self):
        return f"Notification for {self.user.email}: {self.message}"
