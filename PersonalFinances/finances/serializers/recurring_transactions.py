from rest_framework import serializers
from finances.models.recurring_transaction import RecurringTransaction
from finances.serializers.goals import GoalsSerializer

class Recurring_TransactionSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    goals = GoalsSerializer(many=True, read_only=True)

    class Meta:
        model = RecurringTransaction
        fields = ['id', 'user', 'amount', 'category', 'description', 'budget', 'goals', 'transaction_type', 'start_date', 
            'frequency_time', 'next_due_date']
        read_only_fields = ['id']