from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def dashboard_view(request):
    # For now, just render the dashboard template
    return render(request, 'accounts/dashboard.html')

def transaction_list_view(request):
    # Placeholder for transaction list
    return render(request, 'accounts/transactions.html')

def add_transaction_view(request):
    # Placeholder for add transaction
    return render(request, 'accounts/add_transaction.html')

def account_list_view(request):
    # Placeholder for account list
    return render(request, 'accounts/accounts.html')