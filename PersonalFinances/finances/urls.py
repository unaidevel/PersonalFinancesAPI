from rest_framework.routers import DefaultRouter
from finances import views
from django.urls import path, include

router = DefaultRouter()
router.register(r'transaction', views.TransactionViewSet, basename='transaction_list')
router.register(r'category', views.CategoryViewSet, basename='category')
router.register(r'budget', views.BudgetView, basename='budget')
router.register(r'recurring_transactions', views.RecurringTransactionView, basename='recurring_transactions')
router.register(r'goals', views.GoalsView, basename='goals')


urlpatterns = [
    path('', include(router.urls))
]