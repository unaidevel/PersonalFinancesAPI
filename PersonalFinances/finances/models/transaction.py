from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


TRANSACTION_TYPES = [
    ('income', 'Income'),
    ('expense', 'Expense'),
]

class Transaction(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    budget = models.ForeignKey('Budget', on_delete=models.CASCADE, related_name='transactions', null=True, blank=True)
    transaction_type = models.CharField(choices=TRANSACTION_TYPES, default=None, max_length=15)
    amount = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Transaction of {self.amount} done.'
    


@receiver(post_save, sender=Transaction)
@receiver(post_delete, sender=Transaction)
def update_budget_remaining(sender, instance, **kwargs):
    if instance.budget:
        instance.budget.update_remaining_budget()







