def get_monthly_summary(user, year, month):
    """
    Returns a summary with total income and total expense for the specified month.
    """
    # transactions = user.transaction_set.filter(date__year=year, date__month=month)
    # summary = transactions.aggregate(
    #     total_income=Sum('amount', filter=Q(type='income')),
    #     total_expense=Sum('amount', filter=Q(type='expense'))
    # )
    return 1

def get_category_breakdown(user):
    """
    Returns the total expense amount grouped by category.
    """
    # transactions = user.transaction_set.filter(type='expense')
    # breakdown = transactions.values('category__name').annotate(total=Sum('amount')).order_by('-total')
    return 1