from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Transaction, Account  
from django.contrib.auth.models import User




@receiver(post_save, sender=Transaction)
@receiver(post_delete, sender=Transaction)
def update_budget_remaining(sender, instance, **kwargs):
    if instance.budget:
        instance.budget.update_remaining_budget()
    if hasattr(instance.user, 'account'):
        instance.user.account.update_balance()






@receiver(post_save, sender=User)
def create_user_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)