from django.db.models import Sum, Avg, Count, Max, Min
from django.db.models.functions import TruncMonth, TruncYear, Extract, ExtractMonth, ExtractHour
from django.utils import timezone
from transactions.models import Transaction
from datetime import timedelta
from decimal import Decimal

def get_basic_stats(user, start_date=None, end_date=None):
    queryset = Transaction.objects.filter(user=user)
    if start_date:
        queryset = queryset.filter(date__gte=start_date)
    if end_date:
        queryset = queryset.filter(date__lte=end_date)

    income = queryset.filter(type='income').aggregate(
        total=Sum('amount') or 0,
        avg=Avg('amount') or 0,
        count=Count('id'),
        max=Max('amount') or 0,
        min=Min('amount') or 0
    )

    expenses = queryset.filter(type='expense').aggregate(
        total=Sum('amount') or 0,
        avg=Avg('amount') or 0,
        count=Count('id'),
        max=Max('amount') or 0,
        min=Min('amount') or 0
    )

    return {
        'income': income,
        'expenses': expenses,
        'net': float(income['total'] - expenses['total']),
        'total_transactions': queryset.count()
    }

def get_category_breakdown(user, transaction_type='expense', start_date=None, end_date=None):
    queryset = Transaction.objects.filter(user=user, type=transaction_type)
    if start_date:
        queryset = queryset.filter(date__gte=start_date)
    if end_date:
        queryset = queryset.filter(date__lte=end_date)

    return list(queryset.values('category').annotate(
        total=Sum('amount'),
        count=Count('id'),
        avg=Avg('amount')
    ).order_by('-total'))

def get_monthly_trends(user, months=12):
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30 * months)

    monthly_data = Transaction.objects.filter(
        user=user,
        date__gte=start_date,
        date__lte=end_date
    ).annotate(
        month=TruncMonth('date')
    ).values('month', 'type').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('month', 'type')

    return list(monthly_data)

def get_currency_exposure(user):
    return list(Transaction.objects.filter(user=user).values(
        'currency'
    ).annotate(
        total_amount=Sum('amount'),
        transaction_count=Count('id'),
        original_currency_count=Count('original_currency', distinct=True)
    ).order_by('-total_amount'))

def get_vendor_analysis(user, limit=10):
    return list(Transaction.objects.filter(user=user).values(
        'vendor'
    ).annotate(
        total_spent=Sum('amount'),
        transaction_count=Count('id'),
        avg_transaction=Avg('amount')
    ).order_by('-total_spent')[:limit])

def get_spending_patterns(user):
    queryset = Transaction.objects.filter(user=user, type='expense')
    
    hour_distribution = queryset.annotate(
        hour=ExtractHour('date')
    ).values('hour').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('hour')
    
    dow_distribution = queryset.annotate(
        dow=Extract('date', 'dow')
    ).values('dow').annotate(
        total=Sum('amount'),
        count=Count('id')
    ).order_by('dow')
    
    return {
        'hour_distribution': list(hour_distribution),
        # 'dow_distribution': list(dow_distribution)
    }

def generate_dashboard_data(user, start_date=None, end_date=None):
    return {
        'basic_stats': get_basic_stats(user, start_date, end_date),
        'expense_categories': get_category_breakdown(user, 'expense', start_date, end_date),
        'income_categories': get_category_breakdown(user, 'income', start_date, end_date),
        'monthly_trends': get_monthly_trends(user),
        'currencies': get_currency_exposure(user),
        'top_vendors': get_vendor_analysis(user),
        'patterns': get_spending_patterns(user)
    }