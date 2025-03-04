from django.db import models
from django.contrib.auth.models import User


income_category = [
    ('salary', 'Salary'),
    ('freelance', 'Freelance'),
    ('investments', 'Investments'),
    ('gifts', 'Gifts'),
]


class ExpenseCategories(models.TextChoices):
    rent = 'Rent'
    food = 'Food'
    transport = 'Transport'
    entertainment = 'Entertainment'

TRANSACTION_TYPES = [
    ('income', 'Income'),
    ('expense', 'Expense'),
]

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    category_type = models.CharField(choices=TRANSACTION_TYPES, max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'