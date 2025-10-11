from django.urls import path
from . import views # Import views to connect routes to view functions

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path("deposit/", views.deposit_view, name="deposit"),
    path('about/', views.about, name='about'),
    path('accounts/', views.accounts_index, name='accounts-index'),
    path('clients/signup/', views.signup, name='signup'),
    path('accounts/create/', views.create_account, name="create-account"),
    path('account_form', views.account_form, name="account_form"),
    path('t_history', views.t_history, name="t_history"),
]