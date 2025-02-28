from rest_framework import serializers
from finances.models.recurring_transaction import RecurringTransaction


class Recurring_TransactionSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = RecurringTransaction
        fields = ['id', 'user', 'amount','category','description','budget','transaction_type','start_date','frequency_time','next_due_date']
        read_only_fields = ['id']