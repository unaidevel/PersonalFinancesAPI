from rest_framework import serializers
from finances.models import Category, Transaction, Budget, RecurringTransaction
from django.utils import timezone

#Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'category_type']

    

class BudgetSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    create_date = serializers.HiddenField(default=timezone.now)

    class Meta:
        model = Budget 
        fields = ['id', 'name','total_amount','remaining_budget','description', 'category', 'user', 'create_date', 'end_date']
        read_only_fields = ['id', 'remaining_budget']

    
    # def validate_user(self, value):
    #     if self.context['request'].user != value:
    #         raise serializers.ValidationError('You can only create budget for yourself')
    #     return value
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class TransactionSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        request = self.context.get('request', None)
        super().__init__(*args, **kwargs)

        if request and request.user.is_authenticated:
            self.fields['recurring_transaction'].queryset = RecurringTransaction.objects.filter(user=request.user)

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    
    recurring_transaction = serializers.PrimaryKeyRelatedField(queryset=RecurringTransaction.objects.none(), required=False)
    # external_category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'category', 'transaction_type','budget', 'amount', 'date_created']
        read_only_fields = ['id']
    

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    

class Recurring_TransactionSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = RecurringTransaction
        fields = ['id', 'user', 'amount','category','description','budget','transaction_type','start_date','frequency_time','next_due_date']
        read_only_fields = ['id']