import django_filters
from finances.models import Transaction

class TransactionFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')


    class Meta:
        model = Transaction
        fields = {
            'amount': ['lt', 'gt'],
            'date_created': ['exact', 'year__gt']
        }