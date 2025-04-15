"""
URL configuration for FarmFund project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('addFarm/', views.addFarm, name='addFarm'),
    path('farms/', views.farms, name='farms'),
    path('farm/<int:farm_id>/', views.farm_detail, name='farm_detail'),
    path('add_income_expenditure/', views.add_income_expenditure, name='add_income_expenditure'),
    path('txnHistory/', views.txnHistory, name='txnHistory'),
    path('income/delete/<int:income_id>/', views.delete_income, name='delete_income'),
    path('expenditure/delete/<int:expenditure_id>/', views.delete_expenditure, name='delete_expenditure'),
    path('<str:transaction_type>/edit/<int:transaction_id>/', views.edit_transaction, name='edit_transaction'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
