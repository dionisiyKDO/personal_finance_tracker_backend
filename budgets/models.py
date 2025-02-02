from django.db import models
from django.contrib.auth.models import User
from transactions.models import Category  # Import Category from the transactions app

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    budget_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.user.username} - {self.category.name} Budget"

# Budget Model:

#     user: Associates the budget with a specific user.
#     category: The category the budget applies to.
#     budget_amount: The target spending limit (or income goal) for that category.
#     start_date & end_date: The duration for which the budget is valid.