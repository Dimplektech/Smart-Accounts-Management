from . import views
from django.urls import path

app_name = 'accounts'
urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('transactions/', views.transaction_list_view, name='transaction_list'),
    path('add-transaction/', views.add_transaction_view, name='add_transaction'),
    path('accounts/', views.account_list_view, name='account_list'),
]