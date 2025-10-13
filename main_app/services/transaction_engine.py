from django.db import transaction
from main_app.models import Client, Account, Transaction
from datetime import datetime, timedelta


class TransactionService:
    @staticmethod
    @transaction.atomic
    def deposit(account: Account, amount: float, description: str = "") -> Transaction:
        if amount < 0:
            return None
        else:
            account.balance += amount
            account.save()
            return Transaction.objects.create(
                destination_account = account,
                amount = amount,
                status = Transaction.TransactionStatus.COMPLETED,
                type = Transaction.TransactionTypes.DEPOSIT,
                created_at = datetime.now(),
                description = description,
            )
        
    @staticmethod
    @transaction.atomic
    def withdraw(account: Account, amount: float, description: str = "") -> Transaction:
        if amount < 0:
            return None
        else:
            account.balance -= amount
            account.save()
            return Transaction.objects.create(
                origin_account = account,
                amount = amount,
                status = Transaction.TransactionStatus.COMPLETED,
                type = Transaction.TransactionTypes.WITHDRAWAL,
                created_at = datetime.now(),
                description = description,
            )
    
    @staticmethod
    @transaction.atomic
    def transfer(origin_account: Account, destination_account: Account,
                    amount: float, description: str = "") -> Transaction:
        if amount < 0:
            return None
        else:
            origin_account.balance -= amount
            destination_account.balance += amount

            origin_account.save()
            destination_account.save()

            return Transaction.objects.create(
                origin_account = origin_account,
                destination_account = destination_account,
                amount = amount,
                status = Transaction.TransactionStatus.COMPLETED,
                type = Transaction.TransactionTypes.TRANSFER,
                created_at = datetime.now(),
                description = description,
            )
        