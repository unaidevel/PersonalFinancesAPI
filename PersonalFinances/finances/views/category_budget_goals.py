from rest_framework import viewsets
from finances.models import Category, Budget, Goals
from finances.serializers import CategorySerializer, BudgetSerializer, GoalsSerializer
from finances.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from rest_framework import permissions




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
    

class GoalsView(viewsets.ModelViewSet):
    serializer_class = GoalsSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Goals.objects.all()

    def get_queryset(self):
        return Goals.objects.filter(user=self.request.user)

    def perform_create(self, serializer): 
        serializer.save(user=self.request.user)