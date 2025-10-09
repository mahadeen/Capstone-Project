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

# Import HttpResponse to send text-based responses
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
class Account(LoginRequiredMixin):
    def __init__(self, account_type, created_at, balance, client_id):
        self.account_type = account_type
        self.created_at = created_at
        self.balance = balance
        self.client_id = client_id

@login_required
def accounts_index(request):
    # accounts = Account.objects.filter()
    # return render(request, 'accounts/index.html', {'accounts': accounts})
    pass

def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in
            login(request, user)
            return redirect('accounts')
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
    