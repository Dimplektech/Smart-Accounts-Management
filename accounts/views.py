from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Transaction, Account, Category, Budget



def create_default_data(user):
    """Create default account types and categories for new users"""
    from .models import AccountType, Category_type, Category
    
    # Create default account types (if they don't exist)
    default_account_types = [
        'Checking',
        'Savings', 
        'Credit Card',
        'Cash',
        'Investment',
        'Business'
    ]
    
    for account_type_name in default_account_types:
        AccountType.objects.get_or_create(name=account_type_name)
    
    # Create default category types (if they don't exist)
    income_type, _ = Category_type.objects.get_or_create(name='income')
    expense_type, _ = Category_type.objects.get_or_create(name='expense')
    transfer_type, _ = Category_type.objects.get_or_create(name='transfer')
    
    # Create default income categories for the user
    default_income_categories = [
        ('Salary', '#10b981', 'fas fa-briefcase'),
        ('Freelance', '#059669', 'fas fa-laptop-code'),
        ('Investment', '#047857', 'fas fa-chart-line'),
        ('Business', '#065f46', 'fas fa-store'),
        ('Other Income', '#34d399', 'fas fa-plus-circle'),
    ]
    
    # Create default expense categories for the user
    default_expense_categories = [
        ('Food & Dining', '#ef4444', 'fas fa-utensils'),
        ('Transportation', '#dc2626', 'fas fa-car'),
        ('Entertainment', '#b91c1c', 'fas fa-film'),
        ('Shopping', '#991b1b', 'fas fa-shopping-bag'),
        ('Bills & Utilities', '#7f1d1d', 'fas fa-file-invoice-dollar'),
        ('Healthcare', '#fbbf24', 'fas fa-heartbeat'),
        ('Education', '#f59e0b', 'fas fa-graduation-cap'),
        ('Travel', '#d97706', 'fas fa-plane'),
        ('Groceries', '#92400e', 'fas fa-shopping-cart'),
        ('Rent/Mortgage', '#78350f', 'fas fa-home'),
        ('Insurance', '#451a03', 'fas fa-shield-alt'),
        ('Other Expenses', '#6b7280', 'fas fa-minus-circle'),
    ]
    
    # Create default transfer categories for the user
    default_transfer_categories = [
        ('Account Transfer', '#3b82f6', 'fas fa-exchange-alt'),
        ('Savings Transfer', '#1d4ed8', 'fas fa-piggy-bank'),
    ]
    
    # Create income categories for the user
    for name, color, icon in default_income_categories:
        Category.objects.get_or_create(
            user=user,
            name=name,
            category_type=income_type,
            defaults={
                'color': color,
                'icon': icon,
                'description': f'Default {name.lower()} category'
            }
        )
    
    # Create expense categories for the user
    for name, color, icon in default_expense_categories:
        Category.objects.get_or_create(
            user=user,
            name=name,
            category_type=expense_type,
            defaults={
                'color': color,
                'icon': icon,
                'description': f'Default {name.lower()} category'
            }
        )
    
    # Create transfer categories for the user
    for name, color, icon in default_transfer_categories:
        Category.objects.get_or_create(
            user=user,
            name=name,
            category_type=transfer_type,
            defaults={
                'color': color,
                'icon': icon,
                'description': f'Default {name.lower()} category'
            }
        )
    
    # Create a default checking account for the user
    checking_account_type = AccountType.objects.get(name='Checking')
    Account.objects.get_or_create(
        user=user,
        name='Primary Checking',
        account_type=checking_account_type,
        defaults={
            'account_number': '****0001',
            'initial_balance': 0.00,
            'balance': 0.00,
            'description': 'Your primary checking account',
            'is_active': True
        }
    )
    
    print(f"Default data created for user: {user.username}")

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


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            # Create default financial data for new user
            create_default_data(user)
            
            # Optional: Auto-login the user
            login(request, user)
            
            messages.success(request, f'Welcome {username}! Your account has been created.')
            return redirect('accounts:dashboard')
    else:
        form = UserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back {username}!')
            return redirect('accounts:dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')
