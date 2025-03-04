from rest_framework import serializers
from finances.models.transaction import Transaction
from finances.models.recurring_transaction import RecurringTransaction
from finances.models.goals import Goals
from finances.serializers.category import CategorySerializer
from rest_framework import exceptions
from finances.models.goals import Goals
from finances.models.category import Category
from finances.models.budget import Budget

class TransactionSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    external_category = CategorySerializer(many=True, read_only=True)
    goal = serializers.PrimaryKeyRelatedField(queryset=Goals.objects.none(), required=False, allow_null=True)   #None(): Returning an empty list so we can add the elements we desire.
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.none())
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'category', 'transaction_type', 'goal', 'budget', 'amount', 'date_created',
        'external_category']
        read_only_fields = ['id']
        
    def __init__(self, *args, **kwargs):     #Required to get user queryset instead of returning everything. 
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user:
            self.fields['goal'].queryset = Goals.objects.filter(user=request.user)
            self.fields['category'].queryset = Category.objects.filter(user=request.user)
            self.fields['budget'].queryset = Budget.objects.filter(user=request.user)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
        
    # def validate_goal(self, value):
    #     if self.context['request'].user != value:
    #         raise serializers.ValidationError('You can only see your own goals!')
    #     return value