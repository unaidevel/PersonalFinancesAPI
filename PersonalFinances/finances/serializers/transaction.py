from rest_framework import serializers
from finances.models.transaction import Transaction
from finances.models.recurring_transaction import RecurringTransaction
from finances.models.goals import Goals
from finances.serializers.category import CategorySerializer

class TransactionSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    recurring_transaction = serializers.PrimaryKeyRelatedField(queryset=RecurringTransaction.objects.none(), required=False, allow_null=True)
    external_category = CategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'category', 'transaction_type','budget', 'amount', 'date_created', 'goal', 'external_category', 'recurring_transaction']
        read_only_fields = ['id', 'recurring_transactions']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            self.fields['recurring_transaction'].queryset = RecurringTransaction.objects.filter(user=request.user)
            self.fields['goal'].queryset = Goals.objects.filter(user=request.user)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)