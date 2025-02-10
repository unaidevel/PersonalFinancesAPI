from django.db import models
import uuid
from django.contrib.auth.models import User
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
    ('entertaiment', 'Entertaiment'),
]

TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category_type = models.CharField(choices=TRANSACTION_TYPES, max_length=10)

class Transaction(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    transaction_type = models.CharField(choices=TRANSACTION_TYPES, default=None, max_length=15)
    amount = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)



