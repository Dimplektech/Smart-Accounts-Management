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
from .forms import TransactionForm, AccountForm, CategoryForm, BudgetForm


def create_default_data(user):
    """Create default account types and categories for new users"""
    from .models import AccountType, Category_type, Category

    # Create default account types (if they don't exist)
    default_account_types = [
        "Checking",
        "Savings",
        "Credit Card",
        "Cash",
        "Investment",
        "Business",
    ]

    for account_type_name in default_account_types:
        AccountType.objects.get_or_create(name=account_type_name)

    # Create default category types (if they don't exist)
    income_type, _ = Category_type.objects.get_or_create(name="income")
    expense_type, _ = Category_type.objects.get_or_create(name="expense")
    transfer_type, _ = Category_type.objects.get_or_create(name="transfer")

    # Create default income categories for the user
    default_income_categories = [
        ("Salary", "#10b981", "fas fa-briefcase"),
        ("Freelance", "#059669", "fas fa-laptop-code"),
        ("Investment", "#047857", "fas fa-chart-line"),
        ("Business", "#065f46", "fas fa-store"),
        ("Other Income", "#34d399", "fas fa-plus-circle"),
    ]

    # Create default expense categories for the user
    default_expense_categories = [
        ("Food & Dining", "#ef4444", "fas fa-utensils"),
        ("Transportation", "#dc2626", "fas fa-car"),
        ("Entertainment", "#b91c1c", "fas fa-film"),
        ("Shopping", "#991b1b", "fas fa-shopping-bag"),
        ("Bills & Utilities", "#7f1d1d", "fas fa-file-invoice-dollar"),
        ("Healthcare", "#fbbf24", "fas fa-heartbeat"),
        ("Education", "#f59e0b", "fas fa-graduation-cap"),
        ("Travel", "#d97706", "fas fa-plane"),
        ("Groceries", "#92400e", "fas fa-shopping-cart"),
        ("Rent/Mortgage", "#78350f", "fas fa-home"),
        ("Insurance", "#451a03", "fas fa-shield-alt"),
        ("Other Expenses", "#6b7280", "fas fa-minus-circle"),
    ]

    # Create default transfer categories for the user
    default_transfer_categories = [
        ("Account Transfer", "#3b82f6", "fas fa-exchange-alt"),
        ("Savings Transfer", "#1d4ed8", "fas fa-piggy-bank"),
    ]

    # Create income categories for the user
    for name, color, icon in default_income_categories:
        Category.objects.get_or_create(
            user=user,
            name=name,
            category_type=income_type,
            defaults={
                "color": color,
                "icon": icon,
                "description": f"Default {name.lower()} category",
            },
        )

    # Create expense categories for the user
    for name, color, icon in default_expense_categories:
        Category.objects.get_or_create(
            user=user,
            name=name,
            category_type=expense_type,
            defaults={
                "color": color,
                "icon": icon,
                "description": f"Default {name.lower()} category",
            },
        )

    # Create transfer categories for the user
    for name, color, icon in default_transfer_categories:
        Category.objects.get_or_create(
            user=user,
            name=name,
            category_type=transfer_type,
            defaults={
                "color": color,
                "icon": icon,
                "description": f"Default {name.lower()} category",
            },
        )

    # Create a default checking account for the user
    checking_account_type = AccountType.objects.get(name="Checking")
    Account.objects.get_or_create(
        user=user,
        name="Primary Checking",
        account_type=checking_account_type,
        defaults={
            "account_number": "****0001",
            "initial_balance": 0.00,
            "balance": 0.00,
            "description": "Your primary checking account",
            "is_active": True,
        },
    )

    print(f"Default data created for user: {user.username}")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back {username}!")
            return redirect("accounts:dashboard")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "accounts/login.html")


@login_required
def dashboard_view(request):
    # Get current user's Accounts
    user_accounts = Account.objects.filter(user=request.user, is_active=True)

    # Calculate total balance across all accounts
    total_balance = user_accounts.aggregate(total=Sum("balance"))["total"] or 0
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
        user=request.user, date__gte=current_month, date__lt=next_month
    )

    # Calculate total income and expenses for the current month
    monthly_income = (
        current_month_transactions.filter(transaction_type="income").aggregate(
            total=Sum("amount")
        )["total"]
        or 0
    )

    monthly_expenses = (
        current_month_transactions.filter(transaction_type="expense").aggregate(
            total=Sum("amount")
        )["total"]
        or 0
    )

    # Get recent transactions (last10)
    recent_transactions = current_month_transactions.order_by("-date")[:10]

    # Gets active Budget with Progress
    active_budget = Budget.objects.filter(
        user=request.user,
        is_active=True,
        start_date__lte=timezone.now().date(),
        end_date__gte=timezone.now().date(),
    )
    # Chart data : Get Spending by Category for chart
    category_spending = (
        current_month_transactions.filter(transaction_type="expense")
        .values("category__name")
        .annotate(total=Sum("amount"))
        .order_by("-total")[:6]
    )

    # Chart Data: Monthly Income vs Expenses (last 6 months)
    monthly_data = []
    for i in range(6):
        month_date = now.replace(day=1) - timedelta(days=i * 30)
        month_start = month_date.replace(day=1)
        if month_start.month == 12:
            month_end = month_start.replace(year=month_start.year + 1, month=1)
        else:
            month_end = month_start.replace(month=month_start.month + 1)

        month_transactions = Transaction.objects.filter(
            user=request.user, date__gte=month_start, date__lt=month_end
        )

        month_income = (
            month_transactions.filter(transaction_type="income").aggregate(
                total=Sum("amount")
            )["total"]
            or 0
        )

        month_expenses = (
            month_transactions.filter(transaction_type="expense").aggregate(
                total=Sum("amount")
            )["total"]
            or 0
        )

        monthly_data.append(
            {
                "month": month_start.strftime("%b %Y"),
                "income": float(month_income),
                "expenses": float(month_expenses),
            }
        )

    monthly_data.reverse()  # Show oldest to newest

    # Get active budgets with progress
    active_budgets = Budget.objects.filter(
        user=request.user, is_active=True, start_date__lte=now, end_date__gte=now
    )

    # Account balance distribution
    account_distribution = []
    for account in user_accounts:
        if account.balance > 0:
            account_distribution.append(
                {
                    "name": account.name,
                    "balance": float(account.balance),
                    "type": account.account_type.name,
                }
            )

    context = {
        "accounts": user_accounts,
        "total_balance": total_balance,
        "monthly_income": monthly_income,
        "monthly_expenses": monthly_expenses,
        "recent_transactions": recent_transactions,
        "active_budgets": active_budgets,
        # Chart data
        "category_spending": list(category_spending),
        "monthly_data": monthly_data,
        "account_distribution": account_distribution,
    }

    context = {
        "total_balance": total_balance,
        "monthly_income": monthly_income,
        "monthly_expenses": monthly_expenses,
        "user_accounts": user_accounts,
        "recent_transactions": recent_transactions,
        "category_spending": category_spending,
        "active_budget": active_budget,
        "current_month": current_month.strftime("%B %Y"),
    }

    return render(request, "accounts/dashboard.html", context)


@login_required
def transaction_list_view(request):
    # Get filter parameters from request
    category_filter = request.GET.get("category", "")
    type_filter = request.GET.get("type", "")

    # Base queryset for transactions
    transactions = Transaction.objects.filter(user=request.user)

    # Apply filters if provided
    if category_filter:
        transactions = transactions.filter(category_name=category_filter)

    if type_filter:
        transactions = transactions.filter(transaction_type=type_filter)
    # Order transactions by date, most recent first
    transactions = transactions.order_by("-date")

    # Get all categories for the filter dropdown
    categories = Category.objects.filter(user=request.user).order_by("name")

    context = {
        "transactions": transactions,
        "categories": categories,
        "current_category": category_filter,
        "current_type": type_filter,
    }

    return render(request, "accounts/transactions.html", context)


@login_required
def add_transaction_view(request):
    if request.method == "POST":
        form = TransactionForm(request.POST, request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()

            # Update account balance
            account = transaction.account
            if transaction.transaction_type == "income":
                account.balance += transaction.amount
            elif transaction.transaction_type == "expense":
                account.balance -= transaction.amount
            account.save()

            messages.success(
                request,
                "Transaction added successfully! ${transaction.amount} {transaction.transaction_type} to {account.name}.",
            )
    else:
        form = TransactionForm(request.user)

    return render(request, "accounts/add_transaction.html", {"form": form})


@login_required
def account_list_view(request):
    accounts = Account.objects.filter(user=request.user, is_active=True)
    return render(request, "accounts/accounts.html", {"accounts": accounts})


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")

            # Create default financial data for new user
            create_default_data(user)

            # Optional: Auto-login the user
            login(request, user)

            messages.success(
                request, f"Welcome {username}! Your account has been created."
            )
            return redirect("accounts:dashboard")
    else:
        form = UserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


@login_required
def budget_list_view(request):
    """Display all user Budgets"""
    budgets = Budget.objects.filter(user=request.user).order_by("-start_date")

    # Calculate Summary statistics
    total_budgets = budgets.count()
    active_budgets = budgets.filter(is_active=True).count()
    over_budget_count = sum(1 for budget in budgets if budget.is_over_budget)

    context = {
        "budgets": budgets,
        "total_budgets": total_budgets,
        "active_budgets": active_budgets,
        "over_budget_count": over_budget_count,
    }

    return render(request, "accounts/budget_list.html", context)


@login_required
def add_budget_view(request):
    """Add a new Budget"""
    if request.method == "POST":
        form = BudgetForm(request.user, request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, f"Budget {budget.name} created successfully!")
            return redirect("accounts:budget_list")
        else:
            form = BudgetForm(request.user)

    return render(request, "accounts/add_budget.html", {"form": form})


@login_required
def add_account_view(request):
    """Add a new account"""
    if request.method == "POST":
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()

            messages.success(request, f'Account "{account.name}" created successfully!')
            return redirect("accounts:account_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AccountForm()

    return render(request, "accounts/add_account.html", {"form": form})


@login_required
def account_list_view(request):
    """Display all user accounts"""
    accounts = Account.objects.filter(user=request.user).order_by("-created_at")

    # Calculate summary statistics
    total_accounts = accounts.count()
    total_balance = accounts.aggregate(total=Sum("balance"))["total"] or 0
    active_accounts = accounts.filter(is_active=True).count()

    context = {
        "accounts": accounts,
        "total_accounts": total_accounts,
        "total_balance": total_balance,
        "active_accounts": active_accounts,
    }

    return render(request, "accounts/account_list.html", context)


@login_required
def account_detail_view(request, account_id):
    """Display account details"""
    account = get_object_or_404(Account, id=account_id, user=request.user)

    # Get recent transactions for this account
    recent_transactions = Transaction.objects.filter(account=account).order_by("-date")[
        :10
    ]

    # Calculate monthly statistics
    now = timezone.now()
    current_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    monthly_income = (
        Transaction.objects.filter(
            account=account, transaction_type="income", date__gte=current_month
        ).aggregate(total=Sum("amount"))["total"]
        or 0
    )

    monthly_expenses = (
        Transaction.objects.filter(
            account=account, transaction_type="expense", date__gte=current_month
        ).aggregate(total=Sum("amount"))["total"]
        or 0
    )

    context = {
        "account": account,
        "recent_transactions": recent_transactions,
        "monthly_income": monthly_income,
        "monthly_expenses": monthly_expenses,
    }

    return render(request, "accounts/account_detail.html", context)


@login_required
def budget_list_view(request):
    """Display all user budgets"""
    budgets = Budget.objects.filter(user=request.user).order_by("-start_date")

    # Calculate summary statistics
    total_budgets = budgets.count()
    active_budgets = budgets.filter(is_active=True).count()

    context = {
        "budgets": budgets,
        "total_budgets": total_budgets,
        "active_budgets": active_budgets,
    }

    return render(request, "accounts/budget_list.html", context)


@login_required
def add_budget_view(request):
    """Add a new budget"""
    if request.method == "POST":
        form = BudgetForm(request.user, request.POST)
        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()

            messages.success(request, f'Budget "{budget.name}" created successfully!')
            return redirect("accounts:budget_list")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = BudgetForm(request.user)

    return render(request, "accounts/add_budget.html", {"form": form})
