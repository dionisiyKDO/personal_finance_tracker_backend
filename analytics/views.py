from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .utils import get_monthly_summary, get_category_breakdown
from datetime import date

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_data(request):
    user = request.user
    today = date.today()
    monthly_summary = get_monthly_summary(user, today.year, today.month)
    category_breakdown = get_category_breakdown(user)
    return Response({
        'monthly_summary': monthly_summary,
        'category_breakdown': category_breakdown
    })
