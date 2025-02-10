from django.shortcuts import render

from rest_framework import viewsets
from finances.models import Category, Transaction
from finances.serializers import CategorySerializer, TransactionSerializer
from rest_framework import permissions


class CategoryViewSet(viewsets.ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

class TransactionViewSet(viewsets.ModelViewSet):
    
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)