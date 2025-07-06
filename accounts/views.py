from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Transaction, Account, Category, Budget



@login_required
def dashboard_view(request):
    # Get current user's Accounts
    user_accounts = Account.objects.filter(user=request.user, is_active=True)

    # Calculate total balance across all accounts
    total_balance = user_accounts.aggregate(total=Sum('balance'))['total'] or 0
    # For now, just render the dashboard template

    # Get current months date range 
    now = timezone.now()
    current_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Get next month's first day
    if now.month == 12:
        next_month = current_month.replace(year=now.year + 1, month=1)
    else:
        next_month = current_month.replace(month=now.month + 1)
    
    current_month_transactions = Transaction.objects.filter(
        user=request.user,
        date__gte=current_month,
        date__lt=next_month
    )

    # Calculate total income and expenses for the current month
    monthly_income = current_month_transactions.filter(
        transaction_type='income'
        ).aggregate(total=Sum('amount'))['total'] or 0
    
    monthly_expenses = current_month_transactions.filter(
        transaction_type='expense'
    ).aggregate(total=Sum('amount'))['total'] or 0

    # Get recent transactions (last10)
    recent_transactions = current_month_transactions.order_by('-date')[:10]

    # Get Spending by Category for chart
    category_spending = current_month_transactions.filter(
        transaction_type='expense'
    ).values('category__name').annotate(
        total=Sum('amount')
    ).order_by('-total')[:6]

    # Gets active Budget with Progress
    active_budget = Budget.objects.filter(
        user=request.user,
        is_active=True,
        start_date__lte=timezone.now().date(),
        end_date__gte=timezone.now().date()

    )

    context = {
        'total_balance': total_balance,
        'monthly_income': monthly_income,
        'monthly_expenses': monthly_expenses,
        'user_accounts': user_accounts,
        'recent_transactions': recent_transactions,
        'category_spending': category_spending,
        'active_budget': active_budget,
        'current_month': current_month.strftime('%B %Y'),
    }
    
    return render(request, 'accounts/dashboard.html', context)

@login_required
def transaction_list_view(request):
    # Get current user's transactions
    transactions = Transaction.objects.filter(user=request.user).order_by('-date') 
    return render(request, 'accounts/transactions.html', {'transactions': transactions})

@login_required
def add_transaction_view(request):
    # Placeholder for add transaction
    return render(request, 'accounts/add_transaction.html')

@login_required
def account_list_view(request):
    accounts = Account.objects.filter(user=request.user, is_active=True)
    return render(request, 'accounts/accounts.html', {'accounts': accounts})