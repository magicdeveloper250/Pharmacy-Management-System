from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.db.models import Sum
from ..models import Sales, Purchase
from ..decorators import (
    pharmacy_permission_required,
    admin_required,
    superadmin_required,
    staff_required
)
from django.views.decorators.http import require_http_methods

@pharmacy_permission_required('authentication.view_reports')
@require_http_methods(["POST"])
def generate_report(request):
    try:
        report_type = request.POST.get('report_type')
        period_type = request.POST.get('period')
        if period_type == 'custom':
            try:
                start_date = datetime.strptime(request.POST.get('start_date'.replace("/", "-")), '%Y-%m-%d')
                end_date = datetime.strptime(request.POST.get('end_date'.replace("/", "-")), '%Y-%m-%d')
            except (ValueError, TypeError):
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid date format for custom period'
                })
        else:
            end_date = datetime.now()
            if period_type == 'today':
                start_date = end_date.replace(hour=0, minute=0, second=0, microsecond=0)
            elif period_type == 'week':
                start_date = end_date - timedelta(days=7)
            elif period_type == 'month':
                start_date = end_date - timedelta(days=30)
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid period type'
                })

        end_date = end_date + timedelta(days=1)
        if report_type == 'sales':
            queryset = Sales.objects.filter(
                sale_date__gte=start_date,
                sale_date__lt=end_date
            ).values('sale_date').annotate(
                total=Sum('total_price')
            ).order_by('sale_date')
            
        elif report_type == 'purchases':
            queryset = Purchase.objects.filter(
                purchase_date__gte=start_date,
                purchase_date__lt=end_date
            ).values('purchase_date').annotate(
                total=Sum('total_price')
            ).order_by('purchase_date')
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid report type'
            })

        data = list(queryset)
        
        total_amount = sum(item['total'] for item in data)
        avg_amount = total_amount / len(data) if data else 0

        context = {
            'data': [{
                'date': item['sale_date' if report_type == 'sales' else 'purchase_date'],
                'amount': item['total']
            } for item in data],
            'start_date': start_date,
            'end_date': end_date - timedelta(days=1),
            'total_amount': total_amount,
            'average_amount': avg_amount,
            'period_type': period_type,
            'report_type': report_type.capitalize()
        }

        report_html = render_to_string('report.html', context)
        
        period_text = {
            'today': 'Today',
            'week': 'Last 7 Days',
            'month': 'Last 30 Days',
            'custom': f'{start_date.strftime("%Y-%m-%d")} to {end_date.strftime("%Y-%m-%d")}'
        }[period_type]

        return JsonResponse({
            'success': True,
            'report_html': report_html,
            'period': period_text
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error generating report: {str(e)}'
        })