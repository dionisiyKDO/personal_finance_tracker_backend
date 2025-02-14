from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from .models import Transaction
from .serializers import TransactionSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

def get_categories(request):
    categories_map = Transaction.CATEGORY_MAP
    categories = set()
    for string in categories_map.values():
        split_string = string.split("/")
        for s in split_string:
            categories.add(s)
    
    return JsonResponse({"categories": list(categories)})
