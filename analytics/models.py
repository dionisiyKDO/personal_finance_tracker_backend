from django.db.models import Sum, Q
from transactions.models import Transaction

def get_monthly_summary(user, year, month):
    """
    Returns a summary with total income and total expense for the specified month.
    """
    transactions = Transaction.objects.filter(user=user, date__year=year, date__month=month)
    summary = transactions.aggregate(
        total_income=Sum('amount', filter=Q(type='income')),
        total_expense=Sum('amount', filter=Q(type='expense'))
    )
    return summary

def get_category_breakdown(user):
    """
    Returns the total expense amount grouped by category.
    """
    transactions = Transaction.objects.filter(user=user, type='expense')
    breakdown = transactions.values('category__name').annotate(total=Sum('amount')).order_by('-total')
    return breakdown

# Explanation:

#     get_monthly_summary:
#       Filters transactions for the given user and month, then aggregates totals for incomes and expenses.
#     get_category_breakdown:
#       Filters for expense transactions, groups by category name, and sums the amount per category.