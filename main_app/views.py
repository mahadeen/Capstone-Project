from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from main_app.models import Client, Account, Transaction
from main_app.services.transaction_engine import TransactionService
import json
from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from datetime import datetime, timedelta
from django.views.generic.edit import CreateView, UpdateView, DeleteView



class Home(LoginView):
    template_name = 'home.html'


@csrf_exempt
@login_required
def deposit_view(request): # for testing purposes.
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

        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        matches = password1 == password2 and password1 != "" and password1 != None and username != "" and username != None and len(password1) > 3

        existing = Client.objects.filter(username = username)

        is_unique = len(existing) == 0
        
        if is_unique == True and matches == True: 
            client = Client.objects.create(username = username, password = make_password(password1))

            login(request, client)
            return redirect('accounts-index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)


@login_required
def create_account(request):
    print(request.POST.dict())
    account_type = request.POST.get('account_type')
    valid_type = account_type == Account.AccountType.SAVINGS or account_type == Account.AccountType.CHECKING
    if valid_type == False:
        return render (request, 'account_form.html')

    error_message = ''
    if request.method == 'POST':
        account = Account.objects.create(
        client=request.user,
        account_type = account_type,
        balance = 0,
        )
        return redirect('accounts-index')
    else:
        error_message = 'Invalid - try again'

@login_required
def account_form(request):
    accounts = Account.objects.filter(client=request.user)
    return render(request, 'account_form.html')


@login_required
def t_history(request):
    origin_trans = Transaction.objects.filter(
        origin_account__client=request.user
    )
    destination_trans = Transaction.objects.filter(
        destination_account__client=request.user
    )
    all_transactions = origin_trans.union(destination_trans)
    return render(request, 'accounts/t-history.html', {'transactions': all_transactions})

@login_required
def transaction_form(request):
    transaction_type = request.GET.get('transaction_type')
    return render(request, 'transaction_form.html', {'transaction_type': transaction_type})

@login_required
def initiate_transaction(request):
    if request.method == 'POST':

        transaction_type = request.POST.get('transaction_type')
        if not transaction_type:
            return render(request, 'transaction_form.html', {
                'error_message': 'Transaction type is required.'
            })
        amount = request.POST.get('amount')
        amount = int(amount)
        origin_account = request.POST.get('origin_account')
        destination_account = request.POST.get('destination_account')
        description = request.POST.get('description')
        valid = amount > 0
        if transaction_type == Transaction.TransactionTypes.TRANSFER:
            if not origin_account or not destination_account:
                return render(request, 'transaction_form.html')

            origin_account = int(origin_account)
            destination_account = int(destination_account)
            origin_account = Account.objects.get(id=origin_account)
            destination_account = Account.objects.get(id=destination_account)
            
            if valid:
                transaction = TransactionService.transfer(origin_account, destination_account, amount, description)
                return redirect('accounts-index')
            return render(request, 'transaction_form.html')

        elif transaction_type == Transaction.TransactionTypes.DEPOSIT:
            if destination_account:
                destination_account = int(destination_account)
                destination_account = Account.objects.get(id=destination_account)
                if valid:
                    transaction = TransactionService.deposit(account=destination_account, amount=amount, description=description)
                    return redirect('accounts-index')
            return render(request, 'transaction_form.html')
            
        elif transaction_type == Transaction.TransactionTypes.WITHDRAWAL:
            if origin_account:
                origin_account = int(origin_account)
                origin_account = Account.objects.get(id=origin_account)
                if valid:
                    transaction = TransactionService.withdraw(account=origin_account, amount=amount, description=description)
                    return redirect('accounts-index')
            return render(request, 'transaction_form.html')
        
    #     return render(request, 'transaction_form.html', {
    #         'error_message': 'Invalid transaction type or missing input.'
    #     })
        
    # return render(request, 'transaction_form.html')