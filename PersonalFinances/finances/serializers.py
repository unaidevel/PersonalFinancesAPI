from rest_framework import serializers
from finances.models import Category, Transaction, Budget
from django.utils import timezone


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

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    external_category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'category', 'transaction_type','budget', 'amount', 'date_created', 'external_category']
        read_only_fields = ['id']

    # def validate_user(self, value):
    #     if self.context['request'].user != value:
    #         raise serializers.ValidationError('You can only create transactions for yourself.')   
    #     return value
    

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)