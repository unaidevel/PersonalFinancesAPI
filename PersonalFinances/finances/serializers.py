from rest_framework import serializers
from finances.models import Category, Transaction

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'category_type']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['user', 'category', 'transaction_type', 'amount', 'date_created']

    def validate_user(self, value):
        if self.context['request'].user != value:
            raise serializers.ValidationError('You can only create transactions for yourself.')   
        return value