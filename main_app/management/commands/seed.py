from django.core.management.base import BaseCommand
from main_app.models import Client, Account, Transaction
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        
        Transaction.objects.all().delete()
        Account.objects.all().delete()
        Client.objects.all().delete()

        client = Client.objects.create(
            first_name="Abd",
            last_name="Mahadeen",
            username="mahadeen",
            password="1234",
            created_at=datetime.now()
        )
        
        account1 = Account.objects.create(
            client=client,
            account_type = Account.AccountType.CHECKING,
            created_at = datetime.now()
        )
        account2 = Account.objects.create(
            client=client,
            account_type = Account.AccountType.SAVINGS,
            created_at = datetime.now()
        )

        transaction = Transaction.objects.create(
            destination_account = account1,
            amount = 1000,
            status = Transaction.TransactionStatus.COMPLETED,
            type = Transaction.TransactionTypes.DEPOSIT,
            created_at = datetime.now()
        )

        account1.balance += transaction.amount
        account1.save()
