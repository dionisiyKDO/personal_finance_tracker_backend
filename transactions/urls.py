from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, get_categories

router = DefaultRouter()
router.register(r'', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('categories/', get_categories, name='categories'),
    
    path('', include(router.urls)),
]

# http://127.0.0.1:8000/transactions/ (GET, POST)
# http://127.0.0.1:8000/transactions/<id>/ (GET, PUT, DELETE)

# GET     /transactions/ - List all transactions
# POST    /transactions/ - Create a new transaction
# GET     /transactions/{id}/ - Retrieve a transaction
# PUT     /transactions/{id}/ - Update a transaction
# DELETE  /transactions/{id}/ - Delete a transaction
