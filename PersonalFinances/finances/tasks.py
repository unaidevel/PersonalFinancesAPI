from celery import shared_task
from .models import RecurringTransaction


@shared_task
def process_recurring_transactions():
    for transaction in RecurringTransaction.objects.all():
        transaction.frequency()