from django.shortcuts import render
from rest_framework import viewsets
from finances.models import Category, Transaction, Budget, RecurringTransaction
from finances.serializers import CategorySerializer, TransactionSerializer, BudgetSerializer, Recurring_TransactionSerializer
from rest_framework import permissions
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from finances.permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action


#ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        transaction_type = self.request.query_params.get('transaction_type', None)
        if transaction_type:
            return self.queryset.filter(category_type=transaction_type)
        return self.queryset

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

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
            transactions = self.queryset.filter(transaction_type=transaction_type)    
        else:
            transaction = self.queryset
        serializer = self.get_serializer(transaction, many=True)
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