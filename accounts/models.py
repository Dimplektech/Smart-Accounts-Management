from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to="profile_pictures/", blank=True)
    currency = models.CharField(max_length=3, default="GBP")  # Default to GBP
    timezone = models.CharField(max_length=50, default="GMT")  # Default to GMT
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class AccountType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="accounts")
    account_type = models.ForeignKey(
        AccountType, on_delete=models.CASCADE, related_name="accounts_type"
    )
    name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(
        max_digits=15, decimal_places=2, default=Decimal("0.00")
    )
    initial_balance = models.DecimalField(
        max_digits=15, decimal_places=2, default=Decimal("0.00")
    )
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} - {self.account_number} - ${self.balance}"


class Category_type(models.Model):
    CATEGORY_TYPES = [
        ("income", "Income"),
        ("expense", "Expense"),
        ("transfer", "Transfer"),
    ]
    name = models.CharField(max_length=50, choices=CATEGORY_TYPES, unique=True)

    def __str__(self):
        return self.get_name_display()


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=100)
    category_type = models.ForeignKey(
        Category_type, on_delete=models.CASCADE, related_name="categories"
    )
    color = models.CharField(max_length=7, default="#007bff")  # Default to blue color
    icon = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ["user", "name", "category_type"]
        ordering = ["category_type", "name"]

    def __str__(self):
        return f"{self.name} ({self.category_type.name})"


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("income", "Income"),
        ("expense", "Expense"),
        ("transfer", "Transfer"),
    ]

    PAYMENT_METHODS = [
        ("cash", "Cash"),
        ("card", "Card"),
        ("bank_transfer", "Bank Transfer"),
        ("online", "Online Payment"),
        ("check", "Check"),
        ("other", "Other"),
    ]
