from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main_app.models import Account
from main_app.services.transaction_engine import TransactionService
import json
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from main_app.models import Client
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse

class Home(LoginView):
    template_name = 'home.html'

@csrf_exempt
@login_required
def deposit_view(request):
    account1 = Account.objects.get(id=2)
    account2 = Account.objects.get(id=3)
    TransactionService.transfer(account1, account2, 50, "test")
    return JsonResponse({'success': True})

def about(request):
    return render(request, 'about.html')

@login_required
class AccountView(LoginRequiredMixin):
    def __init__(self, account_type, created_at, balance, client_id):
        self.account_type = account_type
        self.created_at = created_at
        self.balance = balance
        self.client_id = client_id

@login_required
def accounts_index(request):
    accounts = Account.objects.filter(client=request.user)
    return render(request, 'accounts/index.html', {'accounts': accounts})
    

def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser

        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        matches = password1 == password2 and password1 != "" and password1 != None and username != "" and username != None and len(password1) > 3

        existing = Client.objects.filter(username = username)

        is_unique = len(existing) == 0
        
        if is_unique == True and matches == True: 
            client = Client.objects.create(username = username, password = make_password(password1))
            
            # This is how we log a user in
            login(request, client)
            return redirect('accounts-index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)
    # Same as: 
    # return render(
    #     request, 
    #     'signup.html',
    #     {'form': form, 'error_message': error_message}
    # )