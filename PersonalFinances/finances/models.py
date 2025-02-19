from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
import datetime



income_category = [
    ('salary', 'Salary'),
    ('freelance', 'Freelance'),
    ('investments', 'Investments'),
    ('gifts', 'Gifts'),
]

expense_categories = [
    ('rent', 'Rent'),
    ('food', 'Food'),
    ('transport', 'Transport'),
    ('entertainment', 'Entertainment'),
]

TRANSACTION_TYPES = [
    ('income', 'Income'),
    ('expense', 'Expense'),
]

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category_type = models.CharField(choices=TRANSACTION_TYPES, max_length=10)

    def __str__(self):
        return f'{self.name}'

class Budget(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=100)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    remaining_budget = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(max_length=500, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Budget: {self.name} for {self.total_amount}. Remaining:{self.remaining_budget}'

    
    def clean(self):
        if self.remaining_budget < 0:
            raise ValidationError({"remaining_budget": "Remaining budget cannot be negative"})
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.remaining_budget = self.total_amount
        super().save(*args, **kwargs)


    def update_remaining_budget(self):
        transactions = Transaction.objects.filter(budget=self)
        total_spent = transactions.aggregate(Sum('amount'))['amount__sum'] or 0
        self.remaining_budget = self.total_amount - total_spent
        self.save()


class Transaction(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
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



FREQUENCY_CHOICES = [
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
]


class RecurringTransaction(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255)
    description = models.CharField(max_length=100)
    budget = models.ForeignKey('Budget', on_delete=models.CASCADE, related_name='Recurring_transaction', null=True, blank=True)
    transaction_type = models.CharField(choices=TRANSACTION_TYPES, max_length=15)  # Corrected this line
    start_date = models.DateField(auto_now_add=True)
    frequency_time = models.CharField(choices=FREQUENCY_CHOICES, default=None, max_length=15)
    next_due_date = models.DateField()

    def __str__(self):
        return f'Recurring transaction of {self.category} created.'
    
    def save(self, *args, **kwargs):
        if not self.next_due_date:
            self.next_due_date = self.calculate_next_due_date()
        super().save(*args, **kwargs)
    
    def calculate_next_due_date(self):
        if self.frequency == 'daily':
            return self.start_date + timezone.timedelta(days=1)
        elif self.frequency == 'weekly':
            return self.start_date + timezone.timedelta(weeks=1)
        elif self.frequency == 'monthly':
            return self.start_date + timezone.timedelta(weeks=4, days=2)
        return self.start_date
