from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .utils import generate_dashboard_data
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from django.core.serializers.json import DjangoJSONEncoder
import json

class DecimalJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        if isinstance(obj, timezone.datetime):
            return obj.isoformat()
        return super().default(obj)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_data(request):
    try:
        user = request.user
        
        # Get time period
        end_date = timezone.now()
        period = request.GET.get('period', 'all')
        
        if period == '7d':
            start_date = end_date - timedelta(days=7)
        elif period == '30d':
            start_date = end_date - timedelta(days=30)
        elif period == '90d':
            start_date = end_date - timedelta(days=90)
        elif period == '1y':
            start_date = end_date - timedelta(days=365)
        elif period == 'all':
            start_date = None
        else:
            try:
                start_date = request.GET.get('start_date')
                if start_date:
                    start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d')
                else:
                    start_date = end_date - timedelta(days=30)
            except ValueError:
                return Response({
                    'error': 'Invalid date format. Use YYYY-MM-DD'
                }, status=400)

        # Get dashboard data
        data = generate_dashboard_data(user, start_date, end_date)
        
        # Convert to JSON-serializable format
        json_data = json.loads(
            json.dumps(data, cls=DecimalJSONEncoder)
        )
        
        return Response({
            'data': json_data,
            'period': {
                'start_date': start_date.isoformat() if start_date else None,
                'end_date': end_date.isoformat()
            }
        })

    except Exception as e:
        import traceback
        print(traceback.format_exc())  # For debugging
        return Response({
            'error': str(e)
        }, status=500)