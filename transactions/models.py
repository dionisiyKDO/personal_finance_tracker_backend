from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50)
    # Optional: If you want categories to be user-specific, associate with a user.
    # Leave blank (or null) for global categories.
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('expense', 'Expense'),
        ('income', 'Income'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    # Allow blank=True if a transaction might not have a category assigned.
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.get_type_display()} - {self.amount}"

# Category Model:

#     name: Holds the category’s name (e.g., “Food”, “Salary”).
#     user: (Optional) Links a category to a specific user. If left null or blank, you can treat the category as a global option.

# Transaction Model:

#     user: Each transaction is tied to a user.
#     amount: A decimal field to store monetary values.
#     type: A choice field to indicate if the transaction is an expense or income.
#     category: A foreign key linking to a Category. Uses SET_NULL so that if a category is deleted, the transaction isn’t removed.
#     description: Additional text details about the transaction.
#     date: The date the transaction occurred.