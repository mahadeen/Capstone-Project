from django.urls import path
from . import views # Import views to connect routes to view functions

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path("deposit/", views.deposit_view, name="deposit"),
    path('about/', views.about, name='about'),
    path('accounts/', views.accounts_index, name='accounts-index'),
    path('clients/signup/', views.signup, name='signup'),
]