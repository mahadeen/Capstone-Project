from django.db import models

# Create your models here.
    
class Client(models.Model):
    first_name = models.CharField(max_length = 100, null=True)
    last_name = models.CharField(max_length = 100, null=True)
    username = models.CharField(max_length = 100, unique=True)
    password = models.CharField(max_length = 100, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    
class Account(models.Model):

    class AccountType:
        CHECKING = "Checking"
        SAVINGS = "Savings"


    client = models.ForeignKey(Client, related_name="accounts", on_delete=models.DO_NOTHING, null=True)
    account_type = models.CharField(max_length = 100, null=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

class Transaction(models.Model):

    class TransactionTypes:
        DEPOSIT = "Deposit"
        WITHDRAWAL = "Withdrawal"
        TRANSFER = "Transfer"
    
    class TransactionStatus:
        COMPLETED = "Completed"
        PENDING = "Pending"
        FAILED = "Failed"

    origin_account = models.ForeignKey(Account, null=True, related_name="outgoing_transactions", on_delete=models.DO_NOTHING)
    destination_account = models.ForeignKey(Account, null=True, related_name="incoming_transactions", on_delete=models.DO_NOTHING)

    amount = models.DecimalField(max_digits=12, decimal_places=2, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    status = models.CharField(max_length=100, default = TransactionStatus.PENDING, null=True)
    type = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

