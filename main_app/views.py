from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main_app.models import Account
from main_app.services.transaction_engine import TransactionService
import json
from django.http import HttpResponse

# Create your views here.

# Import HttpResponse to send text-based responses
from django.http import HttpResponse


# Define the home view function
def home(request):
    # Send a simple HTML response
    return HttpResponse('<h1>Hello</h1>')

@csrf_exempt
def deposit_view(request):
    account1 = Account.objects.get(id=2)
    account2 = Account.objects.get(id=3)
    TransactionService.transfer(account1, account2, 50, "test")
    return JsonResponse({'success': True})

def about(request):
    return render(request, 'about.html')

def home(request):
    return render(request, 'home.html')

class Account:
    def __init__(self, account_type, created_at, balance, client_id):
        self.account_type = account_type
        self.created_at = created_at
        self.balance = balance
        self.client_id = client_id

def accounts_index(request):
    # accounts = Account.objects.filter()
    # return render(request, 'accounts/index.html', {'accounts': accounts})
    pass