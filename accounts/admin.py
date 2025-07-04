from django.contrib import admin
from .models import UserProfile, AccountType, Account
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(AccountType)
admin.site.register(Account)