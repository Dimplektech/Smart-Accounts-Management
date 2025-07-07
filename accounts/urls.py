from . import views
from django.urls import path
from django.contrib.auth import views as auth_views


app_name = 'accounts'
urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('dashboard/', views.dashboard_view, name='dashboard'),

    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path('register/', views.register_view, name='register'),

    # Transaction URLs
    path('transactions/', views.transaction_list_view, name='transaction_list'),
    path('add-transaction/', views.add_transaction_view, name='add_transaction'),
    path('accounts/', views.account_list_view, name='account_list'),
]