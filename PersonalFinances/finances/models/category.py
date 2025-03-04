from django.db import models
from django.contrib.auth.models import User
import uuid

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

def get_default_user():
    user = User.objects.first()
    return user.id if user else None

class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    category_type = models.CharField(choices=TRANSACTION_TYPES, max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_default_user)

    def __str__(self):
        return f'{self.name}'