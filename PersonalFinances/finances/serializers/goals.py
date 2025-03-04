from rest_framework import serializers
from finances.models.goals import Goals


class GoalsSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Goals
        fields = ['id', 'name', 'description', 'target_amount', 'current_amount', 'deadline', 
                  'date_created', 'last_time_edited', 'category', 'user', 'status']
        read_only_fields = ['id', 'date_created', 'status', 'current_amount']
