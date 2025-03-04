from django.shortcuts import render
from rest_framework import viewsets
from finances.models import Category, Transaction, Budget, RecurringTransaction, Goals
from finances.serializers.category import CategorySerializer
from finances.serializers.transaction import TransactionSerializer
from finances.serializers.recurring_transactions import Recurring_TransactionSerializer
# from finances.serializers.spending_insight import SpendingInsightSerializer
from finances.serializers.budget import BudgetSerializer
from finances.serializers.goals import GoalsSerializer
from rest_framework import permissions
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from finances.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from finances.filters import TransactionFilter
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from django.db.models import Sum

#ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        transaction_type = self.request.query_params.get('transaction_type', None)

        queryset = Category.objects.filter(user=self.request.user)
        if transaction_type:
            queryset = queryset.filter(category_type=transaction_type)

        return queryset
class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = TransactionFilter
    filterset_fields = ['amount']
    search_fields = ['amount','category__name']
    ordering_fields = ['amount', 'date_created']

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)
    

    def create(self, request, *args, **kwargs):
        transaction_type = request.data.get('transaction_type')
        category_id = request.data.get('category')
    
        if not Category.objects.filter(id=category_id, category_type=transaction_type).exists():
            return Response(
                {"detail": "Invalid category for the selected transaction type"},
                status=400
            )
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['GET'])
    def filter_by_type(self, request):
        transaction_type = request.query_params.get('transaction_type', None)
        if transaction_type:
            transactions = self.get_queryset().filter(transaction_type=transaction_type)
        else:
            transactions = self.get_queryset()
        serializer = self.get_serializer(transactions, many=True)
        return Response(serializer.data)
    


class BudgetView(viewsets.ModelViewSet):

    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Budget.objects.all()

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)
    

    @action(detail=True, methods=['GET'])
    def transactions(self, request, pk=None):
        budget = self.get_object()
        transacations = budget.transactions.all()
        serializer = TransactionSerializer(transacations, many=True)
        return Response(serializer.data)



class RecurringTransactionView(viewsets.ModelViewSet):
    serializer_class = Recurring_TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = RecurringTransaction.objects.all()

    def get_queryset(self):
        return RecurringTransaction.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GoalsView(viewsets.ModelViewSet):
    serializer_class = GoalsSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Goals.objects.all()

    def get_queryset(self):
        return Goals.objects.filter(user=self.request.user)

    def perform_create(self, serializer): 
        serializer.save(user=self.request.user)



class SpendingListView(ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user=user).order_by('-date_created')

# class InsightList(ListAPIView):

#     serializer_class = SpendingInsightSerializer
#     permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         return Transaction.objects.filter(user=user).order_by('-date_created')
    

class InsightView(ListAPIView):
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user = request.user
        spending_per_category = (
            Transaction.objects.filter(user=user).values('category__name').annotate(total_spent=Sum('amount'))
        )
        return Response(spending_per_category)



class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GitHubLogin(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter
    client_class = OAuth2Client
    # callback_url = TheUrlSetOnGithub


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    # callback_url = TheUrlSetOnGoogle