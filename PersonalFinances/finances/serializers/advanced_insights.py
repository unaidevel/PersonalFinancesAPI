from rest_framework import serializers


# Created this f
class AdvancedInsightsSerializer(serializers.Serializer):

    total_spent_per_month = serializers.ListField(child=serializers.DictField())
    total_sum = serializers.DictField()