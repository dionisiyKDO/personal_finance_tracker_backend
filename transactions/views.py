from rest_framework import viewsets
from .models import Transaction, Category
from .serializers import TransactionSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticated

class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    def get_queryset(self):
        # Return categories that are global or specific to the user.
        return Category.objects.filter(user=self.request.user) | Category.objects.filter(user__isnull=True)
